from socket import socket, AF_INET, SOCK_STREAM
import threading as t
import json

HOST = '127.0.0.1'  #localhost
PORT = 8080
CODING = "utf-8"


def read_request(sock):
    while True:
        data = sock.recv(1024)
        print(json.loads(data.decode(CODING)))


def main():
    clients_list = []
    for i in range(0, (93 - 90) + 23):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((HOST, PORT))
        clients_list.append(sock)

    for client in clients_list:
        listening = t.Thread(target=read_request, args=(client,))
        listening.start()

    while True:
        for client in clients_list:
            client.send(input("enter the number :").encode(CODING))



if __name__ == '__main__':
    main()