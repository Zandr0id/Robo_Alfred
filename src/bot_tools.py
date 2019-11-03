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

def parse_username(line):
    separate = line.split(":", 2)
    username= separate[1].split("!",1)[0]
    return username

def parse_message(line):
    separate = line.split(":", 2)
    message = separate[2]
    return message
