from socket import socket, AF_INET, SOCK_STREAM
import threading as t
import json
import math

HOST = '127.0.0.1'  # localhost
PORT = 8080
CODING = "utf-8"
QUEUE_LEN = 99


def communication(user_socket, user_info, con_num):
    while True:
        number = user_socket.recv(1024)
        number = float(json.loads(number.decode(CODING)))
        number = math.log(number)

        user_socket.send((json.dumps(f'LogN number: {number} , connection number: {con_num.index(user_info[1]+1)}')).encode(CODING))


def main() -> None:
    sock = socket(AF_INET, SOCK_STREAM)

    sock.bind((HOST, PORT))

    sock.listen((93 + 23)-90)

    con_num = []

    while True:
        (user_socket, user_info) = sock.accept()
        con_num.append(user_info[1])
        print(f"user {user_info[0]} connected!")
        user_communication = t.Thread(target=communication, args=(user_socket, user_info, con_num,))
        user_communication.start()

    sock.close()

if __name__ == '__main__':
    main()