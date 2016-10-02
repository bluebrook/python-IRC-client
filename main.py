
import sys
import threading
from console_command_handler import inputHandler
from irc_client import IRCClient

def main():
    argv = sys.argv
    argc = len(sys.argv)
    
    if argc < 3:
        print "Insuficient parameters: host port [nick] [user]" 
        return 1
    host = argv
    port = argv[2]
 
    nick = "MyIRCClient"
    user = "IRCClient"
    
    if argc >= 4:
        nick = argv[3]
    if argc >= 5:
        user = argv[4];
    
    client = IRCClient()
    client.Debug(True)

    #start the input thread
    t = threading.Thread(target=inputHandler, args=[client])
    t.start()
    
    if client.InitSocket():
        print "Socket initialized. Connecting..." 
        if (client.Connect(host, port)):
            print "Connected. Loggin in..." 
            if client.Login(nick, user):
                print "Logged"
                running = True
                while (client.Connected() and running):
                    client.ReceiveData();
            if client.Connected():
                client.Disconnected()
        print "Disconnected"
        
if __name__ == "__main__":
    main()