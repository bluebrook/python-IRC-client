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
        return self._socket is None
    
    def SendData(self, data):
        totalsent = 0
        while totalsent < len(data):
            try:
                sent = self._socket.send(data[totalsent:])
            except OSError as e:
                print e
                return False
            print sent
            if sent == 0:
                raise Exception, "The socket is broken"
            totalsent = totalsent + sent
        return True
    
    def ReceiveData(self, size=1024):
        data = []
        bytes_recd = 0
        while bytes_recd < size:
            try:
                tmp = self._socket.recv(min(size - bytes_recd, 2048))
            except OSError as e:
                print e
                return False
            print tmp
            if tmp == '':
                raise RuntimeError("socket connection broken")
            data.append(tmp)
            bytes_recd = bytes_recd + len(tmp)
        return ''.join(data)


if __name__ == "__main__":
    irs = IRCSocket()
    irs.Init()
    print irs.Connect("chat.freenode.net", 8000)
    print irs.ReceiveData(10)
    irs.SendData("GET \ HTTP\1.1 \n\n")
    print irs.ReceiveData()