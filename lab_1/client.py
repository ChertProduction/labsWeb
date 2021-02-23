from socket import socket, AF_INET, SOCK_STREAM
import threading as t
import json

HOST = '127.0.0.1'          #localhost
PORT = 8080                 # порт
CODING = "utf-8"            # кодування
QUEUE_LEN = (93 + 23)-90    # кількість допустимих підключень


##################################################################################
#функция считывания данных с сервера
#принимает
#sock - сокет
##################################################################################
def readRequest(sock):
    while True:
        data = sock.recv(1024)
        print(json.loads(data.decode(CODING)))                     #зчитуємо формат json

#главная функция
def main():
    USERS = []                                                     #створюємо список клієнтів
    for i in QUEUE_LEN:
        sock = socket(AF_INET, SOCK_STREAM)                        #створємо QUEUE_LEN-у кількість
        sock.connect((HOST, PORT))                                 #сокетів
        USERS.append(sock)                                         #закидуємо їх у список клієнтів

    for user in USERS:                                             #у списку клиентів
        threadClient = t.Thread(target=readRequest, args=(user,))  #створюємо для кожного клієнта поток
        threadClient.start()                                       #запускаемо поток

    while True:
        for user in USERS:                                        #кожному клієнту відправляємо
            user.send(input(">").encode(CODING))                  #запит про введення числа

if __name__ == '__main__':
    main()