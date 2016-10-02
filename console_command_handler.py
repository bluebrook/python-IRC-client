import sys

class ConsoleComandHandler(object):
    
    class CommandEntry(object):
        def __init__(self, func, argc):
            self.argc = argc
            self.func = func
            
    def __init__(self):
        self._commands = {}
    
    def AddCommand(self, name, handler_func, argc):
        if name is None:
            raise Exception, "empty command name"
        self._commands[name.lower()] = ConsoleComandHandler.CommandEntry(handler_func, argc)
    
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
         
        self._commands.get(name)(client, *args)

def msgCommand(client, *args):
    to = args[0]
    text = args[1]
    print "To {}: {}".format(to, text)
    client.sendIRC("PRIVMSG {} :{}".format(to, text))
    
def joinCommand(client, channel):
    if channel[0] != "#":
        channel.insert(0, "#")
    client.sendIRC("JOIN {}".format(channel))

def partCommand(client, channel):
    if channel[0] != "#":
        channel.insert(0, "#")
    client.sendIRC("JOIN {}".format(channel))
    
def ctcpCommand(client, *args):
    to = args[0]
    text = "".join(args)
    print "To {}: {}".format(to, text)
    client.sendIRC("PRIVMSG {} :\001{}\001".format(to, text))

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
        
        if cmdline == "quit":
            break
         
        if cmdline.startswith("/"):
            commandHandler.ParseCommand(cmdline, client)
        else:
            client.sendIRC(cmdline)