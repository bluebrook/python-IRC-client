import irc_socket
from irc_handler import IRCCommandHandler, IRCMessage

class IRCComandPrefix(object):
    ''' A class to parse and hold command prefix 
        The format is nick!user@host
    '''
    def __init__(self):
        self.prefix = ""
        self.nick = ""
        self.user = ""
        self.host = ""
        
    def Parse(self, data):
        if len(data) == 0:
            return 
        
        self.prefix = data.split(" ")[0]
        tokens = []
        if '@' in self.prefix:
            tokens = self.prefix.split('@');
            self.nick = tokens[0]
            self.host = tokens[1]
        
        if '!' in self.prefix:
            tokens = self.nick.split('!')
            self.nick=tokens[0]
            self.user=tokens[1]

class IRCCommandHook(object):
    def __init__(self):
        self.command = None
        self.function = None

class IRCClient(object):
    
    def __init__(self):
        self._socket = irc_socket.IRCSocket()
        self._debug = False
        self._hooks = []
        self._nick = None
        self._user = None
        self.command_handler = IRCCommandHandler(self)
        self.incomplete_msg = ""
        
    def HandleCommand(self, irc_msg):pass
    def CallHook(self, command, irc_msg):pass
    
    def InitSocket(self):
        return self._socket.Init()
        
    def Connect(self, host, port):
        return self._socket.Connect(host, port)
    
    def Disconnect(self):
        self._socket.Disconnect()
        
    def Connected(self):
        return self._socket is not None
    
    def SendIRC(self, data):
        data = data + "\n"
        return self._socket.SendData(data)
        
    def Login(self, nick, user, passwd=""):
        self._nick = nick
        self._user = user 
        
        if self.SendIRC("Hello"):
            if len(passwd) > 0 and not self.SendIRC("PASS " + passwd):
                return False
            if self.SendIRC("NICK " + nick):
                if self.SendIRC("USER " + user + " 8 * :Cpp IRC Client"):
                    return True
                
        return False
    
    def ReceiveData(self):
        buffer = self._socket.ReceiveData()
        lines = buffer.split("\n")
        
        last_line = ""
        if "\r" not in lines[-1]:
            last_line = lines.pop(-1)
        
        if len(lines) > 0:
            if self.incomplete_msg != "":
                lines[0] = self.incomplete_msg + lines[0]
                self.incomplete_msg = ""
            for line in lines:
                line=line.rstrip("\r")
                self.Parse(line)
        
        self.incomplete_msg += last_line
        
    def Parse(self, data):
        
        orig = data[:]
        cmdPrefix = IRCComandPrefix()
        if len(data) == 0:
            return 
        
        #import pdb; pdb.set_trace()
        # parse command prefix
        if data.startswith(":"):
            cmdPrefix.Parse(data[1:])
            data = data[data.find(" ")+1:]
        
        s = data.split(" ", 1)
        command = s[0].upper()
        
        parameters = []
        
        if len(s) > 1:
            data= s[1]
            tmp = data.split(" ")
            for i, item in enumerate(tmp):
                if item.startswith(":"):
                    break
                else:
                    parameters.append(item)
            parameters.append(" ".join(tmp[i:]).lstrip(":"))
        
        if command == 'ERROR':
            print orig
            self.Disconnect()
            return
        
        if command == 'PING':
            print "Ping? Pong"
            self.SendIRC("PONG :" + parameters[0])
            return
        
        irc_msg = IRCMessage(command, cmdPrefix, parameters)
        try:
            self.command_handler.handle(command, irc_msg)
        except Exception as e:
            print orig
            
    def Debug(self, debug):
        self._debug = debug

if __name__ == "__main__":
    tc = IRCClient()
    tc.InitSocket()
    tc.Connect("chat.freenode.net", 8000)
    tc.ReceiveData()
    tc.SendIRC("\list")