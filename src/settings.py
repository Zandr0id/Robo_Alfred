""""
These are the settings the bot uses.
You can connect to any IRC server and channel.
Just provide your own OAUTH key.
Written by Zane Youmans
10/29/2019
"""

import os

HOST = 'irc.twitch.tv'
NICK = 'random' #This doesn't do anything
PASS =  os.environ['OAUTH_KEY'] #your oauth key from your environment
CHANNEL = 'zandr0id_' #your channel
