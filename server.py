import sys
import argparse
import logging
import pathlib
import ssl

import trio
from trio_websocket import serve_websocket, ConnectionClosed


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
here = pathlib.Path(__file__).parent


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Example trio-websocket client")
    parser.add_argument("--ssl", action="store_true", help="Use SSL")
    parser.add_argument(
        "host",
        help="Host interface to bind. If omitted, " "then bind all interfaces.",
        nargs="?",
    )
    parser.add_argument("--port", type=int, help="Port to bind.", default="5678")
    return parser.parse_args()


async def main(args):
    """Main entry point."""
    logging.info("Starting websocket server…")
    if args.ssl:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        try:
            ssl_context.load_cert_chain(here / "fake.server.pem")
        except FileNotFoundError:
            logging.error(
                'Did not find file "fake.server.pem". You need to run'
                " generate-cert.py"
            )
    else:
        ssl_context = None
    host = None if args.host == "*" else args.host
    await serve_websocket(handler, host, args.port, ssl_context)


async def handler(request):
    """Reverse incoming websocket messages and send them back."""
    logging.info(f"Handler starting on path '{request.path}'")

    ws = await request.accept()
    while True:
        try:
            message = await ws.get_message()
            logger.info(message)
            async with trio.lowlevel.FdStream(sys.stdin.fileno()) as stdin:
                breakpoint()
                async for line in stdin:
                    await ws.send_message(line)
        except ConnectionClosed:
            logging.info("Connection closed")
            break

    logging.info("Handler exiting")


if __name__ == "__main__":
    try:
        # async with trio.open_nursery() as nursery:
        #     nursery.start_soon(handler)

        trio.run(main, parse_args())
    except KeyboardInterrupt:
        print()
