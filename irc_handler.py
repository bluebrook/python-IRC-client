class IRCMessage(object):
    ''' store IRC messages '''
    def __init__(self, cmd=None, prefix=None, params=None):
        self.prefix = prefix
        self.command = cmd
        self.parameters = params

class IRCCommandHandler(object):
    ircCommandTable = {}
    
    def __init__(self, client):
        self._client = client
        self.ircCommandTable = {
            "PRIVMSG": IRCCommandHandler.HandlePrivMsg,
            "NOTICE":  IRCCommandHandler.HandleNotice,
            "JOIN":    IRCCommandHandler.HandleChannelJoinPart,
            "PART":    IRCCommandHandler.HandleChannelJoinPart,
            "NICK":    IRCCommandHandler.HandleUserNickChange,
            "QUIT":    IRCCommandHandler.HandleUserQuit,
            "353":     IRCCommandHandler.HandleChannelNamesList,
            "433":     IRCCommandHandler.HandleNicknameInUse,
            "001":     IRCCommandHandler.HandleServerMessage,
            "002":     IRCCommandHandler.HandleServerMessage,
            "003":     IRCCommandHandler.HandleServerMessage,
            "004":     IRCCommandHandler.HandleServerMessage,
            "005":     IRCCommandHandler.HandleServerMessage,
            "250":     IRCCommandHandler.HandleServerMessage,
            "251":     IRCCommandHandler.HandleServerMessage,
            "252":     IRCCommandHandler.HandleServerMessage,
            "253":     IRCCommandHandler.HandleServerMessage,
            "254":     IRCCommandHandler.HandleServerMessage,
            "255":     IRCCommandHandler.HandleServerMessage,
            "264":     IRCCommandHandler.HandleServerMessage,
            "265":     IRCCommandHandler.HandleServerMessage,
            "266":     IRCCommandHandler.HandleServerMessage,
            "366":     IRCCommandHandler.HandleServerMessage,
            "372":     IRCCommandHandler.HandleServerMessage,
            "375":     IRCCommandHandler.HandleServerMessage,
            "376":     IRCCommandHandler.HandleServerMessage,
            "439":     IRCCommandHandler.HandleServerMessage,
        }
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
            print "-" + fr + "- " + text
            
    
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
        params = irc_msg.parameters[1:]

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
    
    def handle(self, command, irc_msg):
        if command not in self.ircCommandTable:
            raise Exception, "no command '{}' found".format(command)
        else:
            self.ircCommandTable[command](self, irc_msg)