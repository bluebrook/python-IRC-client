
import sys
import threading
from console_command_handler import inputHandler
from irc_client import IRCClient
import signal

running = False

def signalHandler(*arg):
    global running
    running = False


def main():
    argv = sys.argv
    argc = len(sys.argv)
    
    if argc < 3:
        print "Insuficient parameters: host port [nick] [user]" 
        return 1
    host = argv[1]
    port = int(argv[2])
    
    print host, port
    nick = "mirrorsymmetry2"
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
                global running
                running = True 
                signal.signal(signal.SIGINT, signalHandler)
                
                while (client.Connected() and running):
                    client.ReceiveData()
            if client.Connected():
                client.Disconnect()
        print "Disconnected"
    
    #t.join()
    
if __name__ == "__main__":
    main()