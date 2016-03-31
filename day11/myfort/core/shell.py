#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import paramiko
import socket
import sys
import os
import traceback
import time
from binascii import hexlify
from paramiko.py3compat import u
from paramiko.py3compat import input
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


class Shell(object):

    def __init__(self, hostname=None, port=None, username=None, password=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.transport = None
        self.channel = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def agent_auth(self):
        agent = paramiko.Agent()
        agent_keys = agent.get_keys()
        if len(agent_keys) == 0:
            return False
        for key in agent_keys:
            print('Trying ssh-agent key %s' % hexlify(key.get_fingerprint()))
            try:
                self.transport.auth_publickey(self.username, key)
                print('... success!')
            except paramiko.SSHException:
                print('... nope.')

    def manual_auth(self):
        default_auth = 'p'
        auth = default_auth
        # auth = input('Auth by (p)assword, (r)sa key, or (d)ss key? [%s] ' % default_auth)
        if len(auth) == 0:
            auth = default_auth
        if auth == 'r':
            default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
            path = input('RSA key [%s]: ' % default_path)
            if len(path) == 0:
                path = default_path
            try:
                key = paramiko.RSAKey.from_private_key_file(path)
            except paramiko.PasswordRequiredException:
                key = paramiko.RSAKey.from_private_key_file(path, self.password)
            self.transport.auth_publickey(self.username, key)
        elif auth == 'd':
            default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_dsa')
            path = input('DSS key [%s]: ' % default_path)
            if len(path) == "0":
                path = default_path
            try:
                key = paramiko.DSSKey.from_private_key_file(path)
            except paramiko.PasswordRequiredException:
                key = paramiko.DSSKey.from_private_key_file(path, self.password)
            self.transport.auth_publickey(self.username, key)
        else:
            self.transport.auth_password(self.username, self.password)

    def run(self):
        paramiko.util.log_to_file("../logs/myfort.log")
        try:
            self.socket.connect((self.hostname, self.port))
        except TimeoutError:
            print("\033[31;1mserver connect timeout\033[0m")
            return False
        except ConnectionRefusedError:
            print("\033[31;1mSSH service not open\033[0m")
            return False
        except Exception:
            traceback.print_exc()
            return False
        try:
            self.transport = paramiko.Transport(self.socket)
            try:
                self.transport.start_client()
            except paramiko.SSHException:
                print('\033[31;1m*** SSH negotiation failed.\033[0m')
                return False
            self.agent_auth()
            if not self.transport.is_authenticated():
                self.manual_auth()
            if not self.transport.is_authenticated():
                print('\033[31;1m*** Authentication failed. :(\033[0m')
                self.transport.close()
                return False
            self.channel = self.transport.open_session()
            self.channel.get_pty()
            self.channel.invoke_shell()
            print('Last login: {} from {}\n'.format(time.ctime(), self.hostname))
            self.interactive_shell()
            self.channel.close()
            self.transport.close()
        except paramiko.BadAuthenticationType:
            print("\033[31;1mUusername or password error\033[0m")
            self.transport.close()
        except Exception:
            traceback.print_exc()
            self.transport.close()

    def interactive_shell(self):
        if has_termios:
            self.posix_shell()
        else:
            self.windows_shell()

    def posix_shell(self):
        import select
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
            self.channel.settimeout(0.0)
            cmd = ""
            while True:
                r, w, e = select.select([self.channel, sys.stdin], [], [])
                if self.channel in r:
                    try:
                        x = u(self.channel.recv(1024))
                        if len(x) == 0:
                            sys.stdout.write('\r\n*** EOF\r\n')
                            break
                        sys.stdout.write(x)
                        sys.stdout.flush()
                    except socket.timeout:
                        pass
                if sys.stdin in r:
                    x = sys.stdin.read(1)
                    if len(x) == 0:
                        print("reak")
                        break
                    if x != "\r":
                        cmd += x
                    else:
                        print(x)
                    self.channel.send(x)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    def writeall(self):
        while True:
            data = self.channel.recv(256)
            if not data:
                sys.stdout.write("\r\n*** EOF ***\r\n\r\n")
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()

    def windows_shell(self):
        import threading
        sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        writer = threading.Thread(target=self.writeall, args=(self.channel,))
        writer.start()
        try:
            while True:
                data = sys.stdin.read(1)
                if not data:
                    break
                self.channel.send(data)
        except EOFError:
            pass

if __name__ == "__main__":
    shell = Shell(hostname='127.0.0.1', port=22, username='zengchunyun', password=' ')
    shell.run()
