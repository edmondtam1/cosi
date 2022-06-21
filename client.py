# import logging
# import pathlib
# import sys
# import trio
# from sys import stderr
# from trio_websocket import open_websocket_url


# async def main():
#     try:
#         async with open_websocket_url("ws://127.0.0.1:8000") as ws:
#             # async with trio.lowlevel.FdStream(sys.stdin.fileno()) as stdin:
#             #     async for line in stdin:
#             #         await ws.send_message(line)
#             # message = await ws.get_message()
#             # print("Client message: %s" % message)
#             await handle_connection(ws, )
#     except OSError as ose:
#         print("Connection attempt failed: %s" % ose, file=stderr)


# async def handle_connection(ws, use_heartbeat):
#     """Connection handler"""
#     logging.debug('Connected!')
#     try:
#         async with trio.open_nursery() as nursery:
#             if use_heartbeat:
#                 nursery.start_soon(heartbeat, ws, 1, 15)
#             nursery.start_soon(get_commands, ws)
#             nursery.start_soon(get_messages, ws)
#     except ConnectionClosed as cc:
#         reason = '<no reason>' if cc.reason.reason is None else f'"{cc.reason.reason}"'
#         print(f'Closed: {cc.reason.code}/{cc.reason.name} {reason}')


# trio.
