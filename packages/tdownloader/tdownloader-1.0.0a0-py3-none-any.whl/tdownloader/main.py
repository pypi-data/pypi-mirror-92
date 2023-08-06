""" Entry point script for tdownloader """

import argparse
import asyncio
import logging
import signal
from functools import partial
from pathlib import Path

from tdownloader.downloader import download

logger = logging.getLogger("TV downloader")
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description="Download parser")
parser.add_argument("input", action="store", help="TXT file with download description")
parser.add_argument("-o", action="store", dest="output_dir", help="Directory to save downloaded files. If not provided "
                                                                  "files will be downloaded to the working directory.")
parser.add_argument("--decompress", action="store_true", help="If specified, the app will try to decompress the files. "
                                                              "(NOT IMPLEMENTED YET!)")
parser.add_argument("-c", "--concurrent-downloads", action="store", dest="concurrent_downloads",
                    help="Concurrent downloads (default 5).", default=5, type=int)

args = parser.parse_args()


def check_args() -> bool:
    """ Check the args are correct. """
    if not Path(args.input).resolve().is_file():
        logger.error(f"{args.input}: File not found!")
        return False
    return True


def banner():
    """ Print a simple banner. """
    print("*" * 80)
    print("TV SHOWS POOL S3 Downloader!")
    print("-" * 80)
    print("Credits: Raydel Miranda <raydel.miranda.gomez@gmail.com>")
    print("*" * 80)


def shutdown(loop):
    """ Stop all. """
    logging.info('Received stop signal, cancelling downloads...')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    logging.info('All download canceled.')


def main():
    """ Entry point. """

    banner()

    if check_args():
        if not args.output_dir:
            output_dir = Path.cwd().resolve()
        else:
            output_dir = Path(args.output_dir).resolve()
        if not output_dir.exists():
            output_dir.mkdir()
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, partial(shutdown, loop))
        loop.add_signal_handler(signal.SIGHUP, partial(shutdown, loop))
        loop.add_signal_handler(signal.SIGINT, partial(shutdown, loop))
        loop.run_until_complete(download(args.input, output_dir, args.concurrent_downloads))
        print("Download complete.")


if __name__ == '__main__':
    main()
