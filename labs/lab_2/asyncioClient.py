from socket import socket, AF_INET, SOCK_STREAM
import asyncio
import json

HOST = '127.0.0.1'           # localhost
PORT = 8080                  # порт
CODING = "utf-8"             # кодування
QUEUE_LEN = (93 + 23)-90

async def readRequest(number):
    reader, writer = await asyncio.open_connection(HOST, PORT)

    message = '{"number":' + number + '}'

    print(f'Send: {message!r}')

    request = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {HOST!r}:{PORT!r}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(message)!r}\r\n"
        f"\r\n"
        f"{message!r}"
    )

    writer.write(request.encode())

    data = await reader.read(1024)
    # print(f'Received: {json.loads(data.decode(CODING))!r}')

    print('Close the connection')
    writer.close()

def main():
    while True:
        asyncio.run(readRequest(input(">")))


if __name__ == '__main__':
    main()