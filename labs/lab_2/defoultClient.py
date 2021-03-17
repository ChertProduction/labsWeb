import asyncio
import json
import math

HOST = '127.0.0.1'           # localhost
PORT = 8080                  # порт
CODING = "utf-8"             # кодування
QUEUE_LEN = (93 + 23)-90

def parseRequest(requestStr):
    rows = requestStr.split("\r\n")

    headers = []
    info = []

    for i in rows:
        if i == "":
            break;
        headers.append(i.split(':')[0])
        info.append(i.split(':')[1])

    mydict = dict(zip(headers, info))
    mydict = json.dumps(mydict)

    object = json.loads(rows[-1])

    # print(f"object[number]: {object['number']}")

    return object

async def readRequest(number):
    reader, writer = await asyncio.open_connection(HOST, PORT)

    message = '{"number":' + number + '}'

    print(f'Send: {message}')

    request = (
        f"Url: GET / HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(message)}\r\n"
        f"\r\n"
        f"{message}"
    )

    writer.write(request.encode())

    data = await reader.read(1024)
    print(data)
    print(parseRequest(data.decode(CODING)))
    # print(f'Received: {json.loads(data.decode(CODING))!r}')

    print('Close the connection')
    writer.close()

def main():
    while True:
        asyncio.run(readRequest(input(">")))


if __name__ == '__main__':
    main()