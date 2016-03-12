#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
       # conn.sendall(bytes(show_list["login"], "utf8"))
       #      time.sleep(0.1)
       #      conn.sendall(bytes("SYN", "utf8"))
       #      option = str(conn.recv(RECV_BUFFER), "utf8")
       #      action = menu.get(option)
       #      if action:
       #          conn.sendall(bytes(show_list["name"], "utf8"))
       #          time.sleep(0.1)
       #          conn.sendall(bytes("SYN", "utf8"))
       #          username = str(conn.recv(RECV_BUFFER), "utf8")
       #          conn.sendall(bytes(show_list["password"], "utf8"))
       #          time.sleep(0.1)
       #          conn.sendall(bytes("SYN", "utf8"))
       #          print(self.rfile.readline())
       #          password = str(conn.recv(RECV_BUFFER), "utf8")
       #          get_result = action(username, password)
       #          while get_result:
       #              time.sleep(0.1)
       #              conn.sendall(bytes(show_list["welcome"], "utf8"))
       #              if read_history(username):
       #                  time.sleep(0.1)
       #                  conn.sendall(bytes(show_list["continue"], "utf8"))
       #                  time.sleep(0.1)
       #                  conn.sendall(bytes("SYN", "utf8"))
       #              else:
       #                  conn.sendall(bytes(show_list["new"], "utf8"))
       #                  time.sleep(0.1)
       #                  conn.sendall(bytes("SYN", "utf8"))
       #          else:
       #              if str(get_result) == str(None):
       #                  logger.info("来自[{}]客户端输入了不存在的用户名,该客户端已被列入锁定对象".format(self.client_address[0]))
       #              else:
       #                  logger.info("来自[{}]客户端输入的密码不正确,该客户端已被列入锁定对象".format(self.client_address[0]))
       #              conn.sendall(bytes(show_list["failed"], "utf8"))
       #              time.sleep(0.1)
       #              conn.sendall(bytes("FIN", "utf8"))
       #      else:
       #          conn.close()
# -*- coding:utf-8 -*-


# def kill_captcha(data):
#     with open('captcha.png','wb') as fp:
#         fp.write(data)
#     return input('captcha:')
#
# import time
# import requests
# from bs4 import BeautifulSoup
#
# def login(username, password, oncaptcha):
#     session = requests.session()
#
#     _xsrf = BeautifulSoup(session.get('https://www.zhihu.com/#signin').content).find('input', attrs={'name': '_xsrf'})['value']
#     captcha_content = session.get('http://www.zhihu.com/captcha.gif?r=%d' % (time.time() * 1000)).content
#     data = {
#         '_xsrf': _xsrf,
#         'email': username,
#         'password': password,
#         'remember_me': 'true',
#         'captcha': oncaptcha(captcha_content)
#     }
#     resp = session.post('http://www.zhihu.com/login/email', data).content
#     assert '\u767b\u9646\u6210\u529f' in resp
#     return session
#
#
# if __name__ == '__main__':
#     session = login('email', 'password', kill_captcha)
#     print(BeautifulSoup(session.get("https://www.zhihu.com").content).find('span', class_='name').getText())


print('\u767b\u9646\u6210\u529f')




       print(self.server.getpeername())
        while True:
            print(online)
            read_sockets, write_sockets, error_sockets = select.select(online_list, [], [])
            for sock in read_sockets:
                if sock == self.server:
                    online_list.append(self.request)
                    print("Client (%s, %s) connected" % self.client_address)
                    broadcast_data(self.request, self.server, "[%s:%s] entered room\n" % self.client_address)
                else:
                    try:
                        data = str(sock.recv(RECV_BUFFER), "utf8")
                        if data:
                            broadcast_data(sock, self.server, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
                    except BrokenPipeError:
                        broadcast_data(sock, self.server, "Client (%s, %s) is offline" % self.client_address)
                        logger.info("来自[{}]客户端,非正常退出,已下线".format(self.client_address[0]))
                        sock.close()
                        online_list.remove(sock)
                        continue
        self.server.close()