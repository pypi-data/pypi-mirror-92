""" Downloader core. """
import asyncio
import concurrent.futures
import logging
from itertools import count
from pathlib import Path
from typing import Optional

import requests
from tqdm import tqdm

from tdownloader.input_file_reader import DownloadTarget, read_file

logger = logging.getLogger("Downloader")
logger.setLevel(logging.INFO)


async def download(input_file: str, dest: Optional[Path], concurrent_downloads: int):
    """ Download the files specified int he input file. """

    loop = asyncio.get_running_loop()
    targets = read_file(input_file)

    counter = count(start=0, step=1)

    for i in range(0, len(targets), concurrent_downloads):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            await asyncio.gather(
                *[loop.run_in_executor(pool, download_target, target, dest, n)
                  for n, target in zip(counter, targets[i:i + concurrent_downloads])]
            )


def download_target(target: DownloadTarget, dest: Path, bar_pos: int) -> Optional[Path]:
    """ Download a single target asynchronously """

    file_size = int(requests.head(target.url).headers['Content-Length'])
    file_path = dest / target.file_name

    initial_size = 0

    if file_path.exists():
        initial_size = file_path.stat().st_size

    # The file has been completely downloaded.
    if initial_size >= file_size:
        return file_path

    header = {"Range": f"bytes={initial_size}-{file_size}"}

    progress_bar = tqdm(total=file_size, initial=initial_size, unit='B', unit_scale=True, desc=target.file_name,
                        unit_divisor=1024, position=bar_pos)

    response = requests.get(target.url, stream=True, headers=header)

    try:
        response.raise_for_status()
    except Exception as err:
        logger.error(f"Error downloading: {target.url}\n{err}")
    else:
        with file_path.open('ab') as destination:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    destination.write(chunk)
                    progress_bar.update(1024)
    finally:
        progress_bar.close()

    return file_path
