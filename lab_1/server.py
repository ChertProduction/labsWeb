from socket import socket, AF_INET, SOCK_STREAM
import threading as t
import json
import math

HOST = '127.0.0.1'           # localhost
PORT = 8080                  # порт
CODING = "utf-8"             # кодування
QUEUE_LEN = (93 + 23)-90     # кількість допустимих підключень


##################################################################################
#функція відправки даних у кліент
#приймає
#sockUser - сокет
#infoUser - інформацію про кліента ( звідси витягуємо номер подключення )
#connectUser - список подключених кліентів
##################################################################################
def sendRequest(sockUser, infoUser, connectUser):
    while True:
        data = sockUser.recv(1024)                      #постійно відправляємо, підтримуємо з'єдання
        data = float(json.loads(data.decode(CODING)))   #створюємо data у json форматі
        data = math.log(data)                           #вичисляємо логарифм натуральний
        sockUser.send((json.dumps(f'Client №{connectUser.index(infoUser[1]+1)} Result: {data}')).encode(CODING))
                                                        #відправляєм клієнту у json форматі результат
                                                        #обчислень й номер підключення ( номер кліента )

#головна функція
def main() -> None:
    sock = socket(AF_INET, SOCK_STREAM)                 #створюмо сокет
    sock.bind((HOST, PORT))                             #отримуємо хост і порт
    sock.listen(QUEUE_LEN)                              #приймає з'єднання

    connectUser = []                                    #список с юзерами

    while True:
        (sockUser, infoUser) = sock.accept()            #повертаємо новий сокет та адресу клієнта
        connectUser.append(infoUser[1])                 #додаємо підключеного юзера у список клієнітв
        print(f"{infoUser[0]} connected!")              #оголошуємо про коректне підключення
        threadUser = t.Thread(target=sendRequest, args=(sockUser, infoUser, connectUser,))
                                                        #створюємо потоки для кожного клієнта,
                                                        #( один потік - один клієнт )
                                                        #у якому працює функція sendRequest()
        threadUser.start()                              #запускаємо потоки

    sock.close()                                        #закриваемо сокет

if __name__ == '__main__':
    main()