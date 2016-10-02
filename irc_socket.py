import socket

class IRCSocket(object):
    def __init__(self):
        self._socket =None

    def Init(self):
        try:
            self._socket = socket.socket(socket.AF_INET, 
                socket.SOCK_STREAM, 
                socket.IPPROTO_TCP)
        except OSError as e:
            print e
            return False
        self._socket.setblocking(0)
        
        import fcntl,os
        fcntl.fcntl(self._socket, fcntl.F_SETFL, os.O_ASYNC)
        return True
    
    def Connect(self, host, port):
        try:
            self._socket.connect((host,port))
        except OSError as e:
            print e
            return False
        return True
    
    def Disconnect(self):
        self._socket.close()
        self._socket = None
        
    def Connected(self):
        return self._socket is not None
    
    def SendData(self, data):
        totalsent = 0
        while totalsent < len(data):
            try:
                sent = self._socket.send(data[totalsent:])
            except OSError as e:
                print e
                return False
            #print sent
            if sent == 0:
                raise Exception, "The socket is broken"
            totalsent = totalsent + sent
        return True
    
    def ReceiveData(self, size=4096):
        if self.Connected():
            return self._socket.recv(size)
        else:
            return ""


if __name__ == "__main__":
    irs = IRCSocket()
    irs.Init()
    print irs.Connect("chat.freenode.net", 8000)
    print irs.ReceiveData(10)
    irs.SendData("GET \ HTTP\1.1 \n\n")
    print irs.ReceiveData()