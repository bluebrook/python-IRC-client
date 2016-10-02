from irc_client import IRCClient


class IRCMessage(object):
    ''' store IRC messages '''
    def __init__(self, cmd=None, prefix=None, params=None):
        self.prefix = prefix
        self.command = cmd
        self.parameters = params

class IRCCommandHandler(object):
    ircCommandTable = {
        "PRIVMSG": HandlePrivMsg,
        "NOTICE":  HandleNotice,
        "JOIN":    HandleChannelJoinPart,
        "PART":    HandleChannelJoinPart,
        "NICK":    HandleUserNickChange,
        "QUIT":    HandleUserQuit,
        "353":     HandleChannelNamesList,
        "433":     HandleNicknameInUse,
        "001":     HandleServerMessage,
        "002":     HandleServerMessage,
        "003":     HandleServerMessage,
        "004":     HandleServerMessage,
        "005":     HandleServerMessage,
        "250":     HandleServerMessage,
        "251":     HandleServerMessage,
        "252":     HandleServerMessage,
        "253":     HandleServerMessage,
        "254":     HandleServerMessage,
        "255":     HandleServerMessage,
        "264":     HandleServerMessage,
        "255":     HandleServerMessage,
        "256":     HandleServerMessage,
        "366":     HandleServerMessage,
        "372":     HandleServerMessage,
        "375":     HandleServerMessage,
        "439":     HandleServerMessage,
    }
    
    def __init__(self, client):
        self._client = client

    def handle(self, command, irc_msg):
        if command not in self.ircCommandTable:
            raise Exception, "no command '{}' found".format(command)
        
        self.ircCommandTable["command"](irc_msg)
        
         
    def HandlePrivMsg(self, irc_msg):
        
        to = irc_msg.parameters[0]
        text = irc_msg.parameters[-1]
        
        if text[0] == '\001':
            self.HandleCTCP(irc_msg)
            return
        
        if to[0] == "#":
            print "From {} @ {}: {}".format(irc_msg.prefix.nick, to, text)
        else:
            print "From {} : {}".format(irc_msg.prefix.nick, text)
    
           
    def HandleNotice(self, irc_msg):
        
        fr = irc_msg.prefix.nick if irc_msg.prefix.nick != "" else irc_msg.prefix.prefix
        text = ""
        if len(irc_msg.parameters) > 1:
            text = irc_msg.parameters[-1]
        
        if text != "" and text.startswith("\001"):
            text = text[1:-2]
            tmp = text.split(" ", 1)
            if len(tmp) == 1:
                print "[Invalid {} reply from {}]".format(text, fr)
            ctcp = tmp[0]
            print "[ {} {} {} reply]: ".format(fr, ctcp, tmp[1])
        else:
            print "-" + fr + "- "
            
    
    def HandleChannelJoinPart(self, irc_msg):
        channel = irc_msg.parameters[0]
        action = "joins" if irc_msg == "JOIN" else "leaves"
        print "{} {} {}".format(irc_msg.prefix.nick, action, channel)
    
    
    def HandleUserNickChange(self, irc_msg):
        newNick = irc_msg.parameters[0]
        print "{} changed his/her nick to {}".format(irc_msg.prefix.nick, newNick)
    
    
    def HandleUserQuit(self, irc_msg):
        text = irc_msg.parameters[0]
        print "{} quits({})".format(irc_msg.prefix.nick, text)
    
    
    def HandleChannelNamesList(self, irc_msg):
        channel = irc_msg.parameters[2]
        nicks = irc_msg.parameters[3]
        print "People on {}:".format(channel)
        print nicks
    
    
    def HandleNicknameInUse(self, irc_msg):
        print "{} {}"(irc_msg.parameters[1],irc_msg.parameters[2])
    
    
    def HandleServerMessage(self, irc_msg):
        params = irc_msg.parameters
        
        if len(params) == 0:
            return
        
        print " ".join(params)
    
    
    def HandleCTCP(self, irc_msg):
        params = irc_msg.parameters
        prefix = irc_msg.prefix
        
        to = params[0]
        text = params[-1]
        text = text[1:-2]
        print "[ {} requested CTCP {}]".format(prefix.nick, text)
        
        if to == self._client._nick:
            if text == "VERSION":
                self._client.SendIRC("NOTICE {} :\001VERSION Open source IRC"
                                     "cleint by Bluebrook \001".format(prefix.nick))
                return
            self._client.SendIRC("NOTICE {} :\001ERRMSG {} :Not implemented\001".format(prefix.nick, text))
