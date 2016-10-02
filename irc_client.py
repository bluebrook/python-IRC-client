import irc_socket
from irc_handler import IRCCommandHandler, IRCMessage

class IRCComandPrefix(object):
    ''' A class to parse and hold command prefix 
        The format is nick!user@host
    '''
    def __init__(self):
        self.prefix = None
        self.nick = None
        self.user = None
        self.host = None
        
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
        
    def HandleCommand(self, irc_msg):pass
    def CallHook(self, command, irc_msg):pass
    
    def InitSocket(self):
        self._socket.Init()
    def Disconnect(self):
        self._socket.Disconnect()
    def Connected(self):
        return self._socket.Connected()
    
    def SendIRC(self, data):
        data = data + "\n"
        self._socket.SendData(data)
        
    def Login(self, nick, user, passwd):
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
        buffer = self.ReceiveData()
        lines = buffer.split("\n")
        for line in lines:
            self.Parse(line.rstrip("\r"))
   
    def Parse(self, data):
        
        orig = data[:]
        cmdPrefix = IRCComandPrefix()
        
        if len(data==0):
            return 
        
        # parse command prefix
        if data[0] == ":":
            cmdPrefix.Parse(data)
            data = data[data.find(" ")+1]
        
        s = data.split(" ", 1)
        command = s[0].lower()
        
        parameters = []
        
        if len(s) > 1:
            data= s[1]
            if data[0] == ":":
                parameters.append(data[1:])
            else:
                pos1 = 0
                pos2 = data.find(" ", pos1)
                while pos2 != -1:
                    parameters.append(data[pos1, pos2-pos1])
                    pos1 = pos2 + 1
                    if (data[pos1] == ":"):
                        parameters.append(data[pos1+1:])
                        break
                    pos2 = data.find(" ", pos1)
                    
                if len(parameters) == 0:
                    parameters.append(data)
                
        
        if command == 'ERROR':
            print orig
            self.Disconnect()
            return
        
        if command == 'PING':
            print "Ping? Pong"
            self.SendIRC("PONG :" + self.parameters[0])
            return
        
        irc_msg = IRCMessage(command, cmdPrefix, parameters)
        
        self.command_handler.handle(command, irc_msg)

    def Debug(self, debug):
        self._debug = debug
