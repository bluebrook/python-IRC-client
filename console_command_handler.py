import sys
import signal

class ConsoleComandHandler(object):
    
    class CommandEntry(object):
        def __init__(self, func, argc):
            self.argc = argc
            self.func = func
            
    def __init__(self):
        self._commands = {}
    
    def AddCommand(self, name, argc, handler):
        if name is None:
            raise Exception, "empty command name"
        self._commands[name.lower()] = ConsoleComandHandler.CommandEntry(handler, argc)
    
    def ParseCommand(self, cmd, client):

        if not self._commands:
            raise Exception, "No command is installed yet"
    
        if cmd[0] == "/":
            cmd = cmd[1:]

        cmdlist = cmd.split(" ")
        name = cmdlist[0].lower()
        
        if name not in self._commands:
            print "Command '{}' not found".format(name)
            return
        
        _command = self._commands.get(name)
        
        if len(cmdlist) > 1:
            args = cmdlist[1:]
        else:
            args = []
            
        if len(args) < _command.argc:
            print "Insufficient argments"
            return
         
        self._commands.get(name).func(client, *args)

def msgCommand(client, *args):
    to = args[0]
    text = " ".join(args[1:])
    text = text.rstrip("\n")
    print "To {}: {}".format(to, text)
    client.SendIRC("PRIVMSG {} :{}".format(to, text))
    
def joinCommand(client, channel):
    if channel[0] != "#":
        channel.insert(0, "#")
    client.SendIRC("JOIN {}".format(channel))

def partCommand(client, channel):
    if channel[0] != "#":
        channel.insert(0, "#")
    client.SendIRC("JOIN {}".format(channel))
    
def ctcpCommand(client, *args):
    to = args[0]
    text = "".join(args)
    print "To {}: {}".format(to, text)
    client.SendIRC("PRIVMSG {} :\001{}\001".format(to, text))

commandHandler = ConsoleComandHandler()

def inputHandler(client):
    commandHandler.AddCommand("msg", 2, msgCommand)
    commandHandler.AddCommand("join", 1, joinCommand)
    commandHandler.AddCommand("part", 2, partCommand)
    commandHandler.AddCommand("ctcp", 2, ctcpCommand)
    while(True):
        try:
            cmdline = sys.stdin.readline()
        except KeyboardInterrupt:
            break
        if cmdline == "":
            continue
        print cmdline
        cmdline.rstrip("\n")
        if cmdline.rstrip("\n") == "quit":
            print "cmdline handler exit"
            sys.exit()
            return
         
        if cmdline.startswith("/"):
            commandHandler.ParseCommand(cmdline, client)
        else:
            client.SendIRC(cmdline)