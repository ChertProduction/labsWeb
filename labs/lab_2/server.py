# import asyncio
# import json
# import math
#
# HOST = '127.0.0.1'           # localhost
# PORT = 8080                  # порт
# CODING = "utf-8"             # кодування
# QUEUE_LEN = (93 + 23)-90
#
# async def handle_echo(reader, writer):
#     # data = await reader.read(1024)
#     # print(data)
#     # message = float(json.loads(data.decode(CODING)))
#     # message = math.log(message)
#     # addr = writer.get_extra_info("peername")
#     #
#     #
#     # print("received %r from %r" % (json.dumps(f'Result: {message}'), addr))
#     # writer.write(json.dumps(f'{message}').encode(CODING))
#
#     # writer.close()
#
#     while True:
#         line = await reader.readline()
#         if not line:
#             break
#
#         line = line.decode('latin1').rstrip()
#         if line:
#             print(f'HTTP header> {line}')
#
#     writer.write(json.dumps(f'{"test": "3001"}').encode('latin1'))
#     await writer.drain()
#     writer.close()
#
# def main():
#     loop = asyncio.get_event_loop()
#     coro = asyncio.start_server(handle_echo, HOST, PORT, loop=loop)
#
#     server = loop.run_until_complete(coro)
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         loop.close()
#         server.close()
#
#
# if __name__ == '__main__':
#     main()

import asyncio

async def handle_echo(reader, writer):
    request = await reader.read(1024)

    message = request.decode()

    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")
    print(f"Send: {message!r}")

    response = (
        f"HTTP/1.1 200 OK\r\n"
        f"\r\n"
        f"{message!r}"
    )

    writer.write(response.encode())
    await writer.drain()

    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8080)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())