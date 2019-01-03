import socket
from threading import Thread
from SocketServer import ThreadingMixIn

TCP_IP = '0.0.0.0'
TCP_PORT = 2004
BUFFER_SIZE = 1024

class ClientThread(Thread):


    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print " New thread started for "+ip+":"+str(port)

    def run(self):
      data = conn.recv(1024)
      print(data.decode(encoding='UTF-8'))
      name=data.decode(encoding='UTF-8')
      name=name.strip('\0')
      print(name)
      with open(name, 'wb') as f:
        print 'file opened'
        while True:
          #print('receiving data...')
          data = self.sock.recv(BUFFER_SIZE)
          if not data:
            print(data)
            f.close()
            print 'file close()'
            break
            # write data to a file
          f.write(data)
      print('Successfully get the file')

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    print 'Got connection from ', (ip,port)
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

