#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import threading
import socket
import selectors
from time import monotonic as time
Selector = selectors.PollSelector


class BaseServer:
    request_queue_size = 5
    allow_reuse_address = False
    timeout = None
    daemon_threads = False

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        self.server_address = server_address
        self.RequestHandlerClass = RequestHandlerClass
        self.__is_shut_down = threading.Event()
        self.__shutdown_request = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if bind_and_activate:
            try:
                self.server_bind()
                self.socket.listen(self.request_queue_size)
            except:
                self.socket.close()
                raise

    def serve_forever(self, poll_interval=0.5):
        self.__is_shut_down.clear()
        try:
            with Selector() as selector:
                selector.register(self, selectors.EVENT_READ)
                while not self.__shutdown_request:
                    ready = selector.select(poll_interval)
                    if ready:
                        self._handle_request_noblock()
                    pass
        finally:
            self.__shutdown_request = False
            self.__is_shut_down.set()

    def shutdown(self):
        self.__shutdown_request = True
        self.__is_shut_down.wait()

    def handle_request(self):
        timeout = self.socket.gettimeout()
        if timeout is None:
            timeout = self.timeout
        elif self.timeout is not None:
            timeout = min(timeout, self.timeout)
        if timeout is not None:
            deadline = time() + timeout
        with Selector() as selector:
            selector.register(self, selectors.EVENT_READ)
            while True:
                ready = selector.select(timeout)
                if ready:
                    return self._handle_request_noblock()
                else:
                    if timeout is not None:
                        timeout = deadline - time()
                        if timeout < 0:
                            pass

    def _handle_request_noblock(self):
        try:
            request, client_address = self.socket.accept()
        except OSError:
            return
        try:
            self.process_request(request, client_address)
        except:
            self.handle_error(request, client_address)
            self.shutdown_request(request)

    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
            self.shutdown_request(request)
        except:
            self.handle_error(request, client_address)
            self.shutdown_request(request)

    def process_request(self, request, client_address):
        t = threading.Thread(target = self.process_request_thread,
                             args = (request, client_address))
        t.daemon = self.daemon_threads
        t.start()

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self)

    def shutdown_request(self, request):
        try:
            request.shutdown(socket.SHUT_WR)
        except OSError:
            pass
        request.close()

    def server_bind(self):
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def fileno(self):
        return self.socket.fileno()

    def handle_error(self, request, client_address):
        print('-'*40)
        print('Exception happened during processing of request from', end=' ')
        print(client_address)
        import traceback
        traceback.print_exc()
        print('-'*40)


class BaseRequestHandler:
    rbufsize = -1
    wbufsize = 0
    timeout = None
    disable_nagle_algorithm = False

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def handle(self):
        pass

    def setup(self):
        if self.timeout is not None:
            self.request.settimeout(self.timeout)
        if self.disable_nagle_algorithm:
            self.request.setsockopt(socket.IPPROTO_TCP,
                                    socket.TCP_NODELAY, True)
        self.rfile = self.request.makefile('rb', self.rbufsize)
        self.wfile = self.request.makefile('wb', self.wbufsize)

    def finish(self):
        if not self.wfile.closed:
            try:
                self.wfile.flush()
            except socket.error:
                pass
        self.wfile.close()
        self.rfile.close()


def main():
    ip_port = ('0.0.0.0', 9999)
    server = BaseServer(ip_port, BaseRequestHandler)
    server.allow_reuse_address = True
    server.serve_forever(poll_interval=0.2)

main()
