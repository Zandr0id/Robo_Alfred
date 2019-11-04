#!/usr/bin/env python3

#test python twitch chat bot

from bot_tools import connect_to_twitch, join_room, send_to_chat, parse
import os
import time

chat = connect_to_twitch()
join_room(chat)
start_time = time.time()

while True:
    read_buffer = chat.recv(2046).decode('utf-8')
    temp = read_buffer.split("\n")
    read_buffer = temp.pop()
    for line in temp:
        if "PING :tmi.twitch.tv" in line:
            chat.send((line.replace("PING","PONG").encode('utf-8')))
            send_to_chat(chat,"I'm awake!")
            print("reply to PING")
        else:
            user = ""
            raw_msg = ""
            cmds = []
            mentions = []
            data = []
            token_msg = []
            user, cmds, mentions, data, token_msg, raw_msg = parse(line) #get all the data out
            
            #make sure there's at least one !command
            if cmds:
                #provide the github link
                print(f"{user} sent: {raw_msg}")
                if(cmds[0] == '!github'):
                    send_to_chat(chat,f"Hey {user}, find the project at {os.environ['TWILIGHT']}")

                #quick blurb about the project
                elif(cmds[0]) == '!project':
                    explanation = "TwilightOS is a scratch-built OS, mainly using C (but going to C++). It is built stand alone (no linux or anything). Use !github for the link!"
                    send_to_chat(chat,explanation)

                #wave at people in the chat    
                elif(cmds[0] == '!wave'):
                    waved_at = ' '
                    if mentions:
                        for mention in mentions:
                            waved_at += (mention + ' ')
                        send_to_chat(chat,f"{user} waves at {waved_at}")
                    else:
                        send_to_chat(chat,f"{user}, you didn't wave at anyone...")

                #link to the bot github to show commands
                elif(cmds[0] == '!commands'):
                    message = f"{user}, you can find the list of commands at the bot github page: {os.environ['ROBO_ALFRED']}"
                    send_to_chat(chat,message)

                #get uptime
                elif(cmds[0] == '!uptime'):
                    up_seconds = (time.time() - start_time)
                    m, s = divmod(up_seconds, 60)
                    h, m = divmod(m, 60)
                    up_time = f"{int(h)} hours, {int(m)} minutes and {int(s)} seconds"
                    message = f"{user}, the stream has been up for {up_time}"
                    send_to_chat(chat,message)
