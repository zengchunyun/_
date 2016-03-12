#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socket,traceback,os,os.path,sys,time,struct,base64,gzip,array,threading
import select,json

'''
{'id','type'}
type - 'mapshow','imageplay'
id - 一次会话的编号
imageplay 与xbridge建立socket连接，并注册一个会话编号(随机产生)
imageplay启动mapshow,并将会话编号传递给mapshow,mapshow建立xbridge的连接，并提交会话编号
xbridge将双向传递相同会话编号的数据到对方

sock1的客户必须等sock2连接进入之后发送数据，否则将sock1数据转发给sock2时将产生异常
'''
 class ConnectionPair:
      def __init__(self,app):
          self.app = app
          self.id = ''
          self.sock1=None #imageplay上来的连接
          self.sock2=None #第二个连接上来的对象mapdemo

      def start(self):
          t = threading.Thread(target=self.threadRecv)
          t.start()

      def onLostConnection(self):
          try:
              print 'connection pair lost..'
              self.sock1.close()
              self.sock2.close()
              self.app.onConnectionPairBroken(self)
          except:
              traceback.print_exc()

      def threadRecv(self):
          print 'service threading entering '
          import select
          while True:
              fds = []
              if self.sock1:
                  fds.append(self.sock1)
              if self.sock2:
                  fds.append(self.sock2)
              #fds = [self.sock1,self.sock2]
              try:
                  #sock2未连接进来前，将不接收sock1上产生数据
                  #print 'fds:',len(fds),fds
                  rds,wds,eds = select.select(fds,[],[],1)
                  if not rds:#timeout
                      continue

                  for s in rds:
                      d = s.recv(1024)
                      #print d
                      if not d:
                          raise 'any jump'

                      to = self.sock2
                      if s == self.sock2:
                          to = self.sock1
                      #print 'redirect data:',d
                      to.sendall(d)
              except:
                  traceback.print_exc()
                  self.onLostConnection()
                  break

          print 'ConnThread Exiting '




  class XBridge:
      def __init__(self,addr=('',12788)):
          self.sock = None
          self.addr = addr
          self.conns={} #{id}
          self.mtxconns = threading.Lock()

      def onConnectionPairBroken(self,cp):
          self.mtxconns.acquire()
          del self.conns[cp.id]
          print 'onConnectionPairBroken(),removed:',cp.id
          self.mtxconns.release()

      def start(self):
          try:

              self.sock = socket.socket()
              #print 'lll',self.addr
              self.sock.bind( tuple(self.addr) )
              self.sock.listen(5)

              self.thread = threading.Thread(target=self.service_loop)
             self.thread.start()
             print 'xbridge started!'
             self.thread.join()
         except:
             traceback.print_exc()
             return False

     def shutdown(self):
         self.sock.close()


     def service_loop(self):

         while True:
             fdr = []
             fdr.append(self.sock)
             infds,wr,e = select.select(fdr,[],[])
             if e:
                 print 'service thread exit '
                 break
             for s in infds:
                 if s == self.sock: #新连接到达
                     sock = None
                     try:
                         sock,peer = self.sock.accept()    #异常产生表示self.sock被强行关闭
                         print 'new client incoming ',peer
                     except:
                         return
                     thread = threading.Thread(target=self.threadNewClient,args=(sock,))
                     thread.start()

     def threadNewClient(self,sock):
         #等待注册信息进入 ，5 秒超时
         try:
             fdr = [sock,]
             print 'enter select  '
             infds,wr,e = select.select(fdr,[],[],5)

             if not infds:
                 sock.close()
                 print 'client register timeout'
                 return #接收超时
             d = sock.recv(1024)
             d = json.loads(d)
             id,type = d['id'],d['type']
             connpair = None
             print id,type
             self.mtxconns.acquire()
             if type == 'imageplay':

                 cp = ConnectionPair(self)
                 cp.id = id
                 cp.sock1 = sock
                 self.conns[id] = cp
                 cp.start()

             elif type =='mapshow':
                 connpair = self.conns.get(id,None)
                 if connpair == None: #没找到imageplay
                     sock.close()
                     print 'mapshow cannt found imageplay..'
                 else:
                     print 'mapclient matched!'
                     connpair.sock2 = sock
             else:
                 print 'unknown command id:',id,type

             self.mtxconns.release()
         except:
             sock.close()
             traceback.print_exc()

 if __name__=='__main__':
     XBridge().start() #default '',12788
