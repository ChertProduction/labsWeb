import selectors
import socket
import json
import math

HOST = '127.0.0.1'           # localhost
PORT = 8080                  # порт
CODING = "utf-8"             # кодування
QUEUE_LEN = (93 + 23)-90

mysel = selectors.DefaultSelector()
keep_running = True

def parseRequest(requestStr):
    rows = requestStr.split("\r\n")

    headers = []
    info = []

    for i in rows:
        if i == "":
            break;
        headers.append(i.split(':')[0])
        print(i.split(':')[0])
        info.append(i.split(':')[1])
        print(i.split(':')[1])

    mydict = dict(zip(headers, info))
    mydict = json.dumps(mydict)

    print(rows)

    object = json.loads(rows[-1])

    data = object['number']

    # print(f"object[number]: {object['number']}")

    data = math.log(data)

    data = json.dumps(f'number:{data}')

    print(data)

    request = (
        f"Url: {info[0]}\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"Content-Type: {info[2]}\r\n"
        f"Content-Length: {info[3]}\r\n"
        f"\r\n"
        f"{data}"
    )

    return request

def read(connection, mask):
    global keep_running

    client_address = connection.getpeername()
    print('read({})'.format(client_address))
    data = connection.recv(1024)
    if data:
        # A readable client socket has data
        print('  received {!r}'.format(data))
        dr = parseRequest(data.decode(CODING))
        connection.sendall(dr.encode(CODING))
    else:
        # Interpret empty result as closed connection
        print('  closing')
        mysel.unregister(connection)
        connection.close()
        # Tell the main loop to stop
        # keep_running = False


def accept(sock, mask):
    new_connection, addr = sock.accept()
    print('accept({})'.format(addr))
    new_connection.setblocking(False)
    mysel.register(new_connection, selectors.EVENT_READ, read)


server_address = (HOST, PORT)
print('starting up on {} port {}'.format(*server_address))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(server_address)
server.listen(QUEUE_LEN)

mysel.register(server, selectors.EVENT_READ, accept)

while keep_running:
    # print('waiting for I/O')
    for key, mask in mysel.select(timeout=1):
        callback = key.data
        callback(key.fileobj, mask)

print('shutting down')
mysel.close()