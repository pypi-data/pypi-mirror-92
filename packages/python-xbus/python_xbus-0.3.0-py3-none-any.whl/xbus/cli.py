import argparse
import asyncio
import logging
import sys
import yaml
import signal
import os.path

from .client import Client

import logging

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog="xbus-python-client",
    description="A python Xbus client",
)

parser.add_argument(
    '-c', '--config', type=argparse.FileType('r'), default="xbus-client.yaml")

parser.add_argument('--debug', action="store_true")


async def serve(client, loop):
    await client.connect(loop)
    await client.startup(loop)


def main():
    options = parser.parse_args(sys.argv[1:])
    logging.basicConfig(level=logging.DEBUG if options.debug else logging.INFO)
    confdict = yaml.load(options.config)
    confdir = None
    if hasattr(options.config, "name"):
        confdir = os.path.dirname(options.config.name)
    client = Client(confdict, confdir)

    loop = asyncio.get_event_loop()
    loop.set_debug(options.debug)
    loop.add_signal_handler(signal.SIGINT, loop.stop)
    t = loop.create_task(serve(client, loop))
    log.info("Client initialization done, now listening...")
    loop.run_forever()
    loop.run_until_complete(client.shutdown())
    loop.run_until_complete(client.close())
    loop.run_until_complete(t)
    loop.close()
