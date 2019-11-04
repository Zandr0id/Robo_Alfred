#!/usr/bin/env python3

"""
A quick and simple IRC bot in python. This bot should work with any IRC server system.
It's very simple, but easy to add more commands to.
Written by Zane Youmans
10/29/2019
"""

from bot_tools import connect_to_twitch, join_room, send_to_chat, parse
import os
import time

chat = connect_to_twitch()
join_room(chat)
start_time = time.time()

try:
    while True:
        read_buffer = chat.recv(2046).decode('utf-8')
        temp = read_buffer.split("\n")
        read_buffer = temp.pop()
        for line in temp:

            #twitch sends pings to make sure we're still there
            #respond to them
            if "PING :tmi.twitch.tv" in line:
                chat.send((line.replace("PING","PONG").encode('utf-8')))
                #the next message in chat always gets skipped...
                #workaround: Send a chat message that never gets printed...
                send_to_chat(chat,"I'm awake!")
                print("reply to PING")

            #any other text, we'll see if there's a command in it    
            else:
                #blank data
                user = ""
                raw_msg = ""
                cmds = []
                mentions = []
                data = []
                token_msg = []

                user, cmds, mentions, data, token_msg, raw_msg = parse(line) #get all the data out
                
                #make sure there's at least one !command
                if cmds:
                    print(f"{user} sent: {raw_msg}")
                    for cmd in cmds:
                        #provide the github link
                        if(cmd == '!github'):
                            send_to_chat(chat,f"Hey {user}, find the project at {os.environ['TWILIGHT']}")
                            break;
                        #quick blurb about the project
                        elif(cmd) == '!project':
                            explanation = "TwilightOS is a scratch-built OS, mainly using C (but going to C++). It is built stand alone (no linux or anything). Use !github for the link!"
                            send_to_chat(chat,explanation)
                            break;
                        #wave at people in the chat    
                        elif(cmd == '!wave'):
                            waved_at = ''
                            if mentions:
                                waved_at += mentions[0]
                                size = len(mentions)
                                print(size)
                                if size > 2:
                                    for mention in mentions[1:(size-1)]:
                                        waved_at += f", {mention}"
                                if size > 1:
                                    waved_at += f" and {mentions[(size-1)]}"
                                send_to_chat(chat,f"{user} waved at {waved_at}")
                            else:
                                send_to_chat(chat,f"{user}, you didn't wave at anyone...")
                            break;
                        #link to the bot github to show commands
                        elif(cmd == '!commands'):
                            message = f"{user}, you can find the list of commands at the bot github page: {os.environ['ROBO_ALFRED']}"
                            send_to_chat(chat,message)
                            break;
                        #get uptime
                        elif(cmd == '!uptime'):
                            up_seconds = (time.time() - start_time)#time diff in seconds
                            m, s = divmod(up_seconds, 60) #get min and sec
                            h, m = divmod(m, 60) #get hours

                            #format the time nicely
                            #I have nothing better to do...
                            if (h == 1):
                                hour_text = f"hour"
                            else:
                                hour_text = f"hours"
                            if (m == 1):
                                minute_text = f"minute"
                            else:
                                minute_text = f"minutes"
                            if (s == 1):
                                second_text = f"second"
                            else:
                                second_text = f"seconds"
                        
                            #construct a string to send
                            up_time = f"{int(h)} {hour_text}, {int(m)} {minute_text} and {int(s)} {second_text}"
                            message = f"{user}, the stream has been up for {up_time}"
                            send_to_chat(chat,message)
                            break;
                        #don't understand...
                        else:
                            print(f"unknown cmd: {cmd}")
                        
except KeyboardInterrupt:
    send_to_chat(chat,"Bye everyone!")
except Exception as e:
    print(e)