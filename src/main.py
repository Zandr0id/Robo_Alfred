#test python twitch chat bot

from bot_tools import connect_to_twitch, join_room, send_to_chat, parse_username, parse_message
from math import factorial

chat = connect_to_twitch()

join_room(chat)

while True:
    read_buffer = chat.recv(2046).decode('utf-8')
    temp = read_buffer.split("\n")
    read_buffer = temp.pop()
    for line in temp:
        print(line)
        if "PING :tmi.twitch.tv" in line:
            chat.send((line.replace("PING","PONG").encode('utf-8')))
            send_to_chat(chat,"I'm awake!")
            print("reply to PING")
        else:
            user = parse_username(line)
            msg = parse_message(line)
            if "!yousuck" in msg:
                send_to_chat(chat,f"No, {user}, you suck!")
            elif "!youpretty" in msg:
                send_to_chat(chat,f"No, {user}, you pretty :)")
            elif "!math" in msg:
                new_msg = msg.split(" ")
                if len(new_msg)==1:
                    send_to_chat(chat,f"{user} you fool! !math needs inputs!")
                else:
                    inputs = new_msg[1].split("+")
                    number = 0
                    for num in inputs:
                        number += (float)(num)
                    send_to_chat(chat,f"{user}, your sum is {number}!")
            elif "!fac" in msg:
                new_msg = msg.split(" ")
                if len(new_msg)==1:
                    send_to_chat(chat,f"{user} you fool! !math needs inputs!")
                else:
                    number = factorial((int)(new_msg[1]))
                    send_to_chat(chat,f"{user}, your factorial is {number}!")
            elif "!sarcasm" in msg:
                send_to_chat(chat,f"{user} is not impressed...")
            elif "!parrot" in msg:
                send_to_chat(chat,msg)
            elif "!uhoh" in msg:
                send_to_chat(chat,"SSSsss")
            elif "!github" in msg:
                send_to_chat(chat,"https://github.com/Zandr0id/TwilightOS")
        
