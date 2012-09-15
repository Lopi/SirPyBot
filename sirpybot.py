#!/usr/bin/env python
'''
Name: sirpybot.py
Description: IRC Bot
Author: ISUSec Members -- Lopi, b0b, polacek, ducky
Version: 0.1
'''
# Libraries
import socket # Communicate with irc server
import sys # CLI options
import os # System calls
import platform # System info gathering
import locale # System language
import urllib2 # Used to get external ip address

# Global variables to configure the bot        
server = sys.argv[1]  # Server
port = sys.argv[2]    # Port
channel = '#' + sys.argv[3] # Channel
botnick = sys.argv[4] # Nickname
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IRC Socket

# Functions are defined below

def banner(): # Displayed when the program starts
  title = 'SirPyBot'
  version = 'Version 0.1'
  contact = 'chris[dot]spehn[at]gmail[dot]com'
  print '\n' + title.center(45)
  print '\n' + version.center(45)
  print '\n' + contact.center(45)

def usage(): # Usage information
  print '\nSirPyBot: You can\'t run SirPyBot using that snytax!'
  print '\nUsage: ./SirPyBot.py server port channel nickname'
  print '\nExample: ./SirPyBot.py irc.freenode.net 6667 isusec SirPyBot'

def ping(): # Function to respond to server pings
  ircsock.send('PONG :pingis\n')

def getlogin(): # Function to get user name
  if (str(platform.platform()))[0:3]=="Win": # If user is running Windows, get username from environment variable %USERNAME% instead
    print 'Sending message -- User name: ' + str(os.getenv("USERNAME"))
    sendmsg(channel, 'User name: ' + str(os.getenv("USERNAME"))) 
  else:
    print 'Sending message -- User name: ' + str(os.getlogin())
    sendmsg(channel, 'User name: ' + str(os.getlogin()))   

def sysinfo(): # Function to obtain system information
  print 'Sending system information'
  sendmsg(channel, 'Computer: ' + platform.uname()[1])
  sendmsg(channel, 'OS: ' + platform.platform()) 
  sendmsg(channel, 'Arch: ' + platform.machine())
  sendmsg(channel, 'Language: ' + locale.getdefaultlocale()[0])

def get_external_ip(): # Function to get external ip address
    ip = urllib2.urlopen('http://automation.whatismyip.com/n09230945.asp').read()
    sendmsg(channel, 'Connecting from ' + ip + ' to serve you master!')

def sendmsg(chan , msg): # Function to send messages to the channel
  ircsock.send('PRIVMSG '+ chan +' :'+ msg +'\n')

def joinchan(chan): # Function to join channels
  ircsock.send('JOIN '+ chan +'\n')

def hello(): # Function responds to a user that inputs 'Hello BotName'
  ircsock.send('PRIVMSG '+ channel +' :Hello!\n')
          
def connect(): # Connects to the server, finds commands, etc.
  ircsock.connect((server, int(port))) # Connect to the server
  ircsock.send('USER ' + botnick + ' ' + botnick + ' ' + botnick + ' :' + botnick + '\n') # User authentication
  ircsock.send('NICK '+ botnick +'\n') # Assign NICK to the bot
  joinchan(channel) # Join the channel

def main():
  os.system('clear') # Clear the screen
  banner() # Print the banner
  connect() # Connect to the server
  get_external_ip()  # Show where the bot is connecting from

  while 1: # WARNING: May cause an infinite loop

    ircmsg = ircsock.recv(2048) # Receive data from the server
    ircmsg = ircmsg.strip('\n\r') # Remove linebreaks
    print(ircmsg) # Print server's messages
  
    if ircmsg.find(':Hello '+ botnick) != -1: # Calls hello() if 'Hello BotName' is found
      hello()

    if ircmsg.find('PING :') != -1: # Respond to server pings
      ping()

    if ircmsg.find(':User '+ botnick) != -1: # Calls getlogin() if 'User BotName' is found
      getlogin()

    if ircmsg.find(':sysinfo '+ botnick) != -1: # Calls sysinfo() if 'sysinfo BotName' is found
      sysinfo()    

    if ircmsg.find(':getip '+ botnick) != -1: # Calls get_external_ip() if 'getip BotName' is found
      get_external_ip()

if __name__ == '__main__':
  if len(sys.argv) != 5:  
    usage()
    sys.exit(1)
  else:
    main()