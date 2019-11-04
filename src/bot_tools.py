import socket
import string
from settings import PASS, NICK, HOST, CHANNEL

def connect_to_twitch():
    s = socket.socket()
    s.connect((HOST,6667))
    s.send(f"PASS {PASS}\r\n".encode('utf-8'))
    s.send(f"NICK {NICK}\r\n".encode('utf-8')) #This does not do anything, but has to be sent anyway
    s.send(f"JOIN #{CHANNEL}\r\n".encode('utf-8'))
    return s

def join_room(chat):
    currently_loading = True
    while currently_loading:
        read_buffer = chat.recv(2046).decode('utf-8')
        temp = read_buffer.split("\n")
        read_buffer = temp.pop()

        for line in temp:
            print(line)
            currently_loading = loading_complete(line)
    send_to_chat(chat,"I have arrived!")

def loading_complete(line):
    if("End of /NAMES list" in line):
        return False
    else:
        return True

def send_to_chat(chat, message):
    message_string = f"PRIVMSG #{CHANNEL} :{message}\r\n"
    encoded_msg = message_string.encode('utf-8')
    chat.send(encoded_msg)
    print("Sent: " + message_string)

def parse(line):
    try:
        back = line.find('!')
        username = line[1:back] #pull out the user who sent this message

        separate = line.split(":", 2)
        message = separate[2] # find the message content

        token_msg = message.split(" ")
        cmds = [] #token list of !cmds
        mentions = [] #token list of @mentions
        data = [] #token list of any other word
        for word in token_msg:
            if (word[0] == '!'): #pull out the first !cmd
                cmds.append(word.replace('\r',''))
            elif (word[0] == '@'): #pull out and @usernames
                mentions.append(word.replace('\r',''))
            else:
                data.append(word.replace('\r','')) #anything else is considered data
        return username, cmds, mentions, data, token_msg, message
    except Exception as e:
        print("Could not parse messge.")
        print(line)
        print(e)
    return username, message