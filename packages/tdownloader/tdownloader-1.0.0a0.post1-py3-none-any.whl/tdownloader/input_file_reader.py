""" Read the input file. """

import csv
from collections import namedtuple
from typing import List
from pathlib import Path

DownloadTarget = namedtuple('DownloadTarget', 'url,file_name')


def read_file(input_file_name: str) -> List[DownloadTarget]:
    """ Read the file and return a list of download targets. """

    path = Path(input_file_name).resolve()

    with path.open() as input_file:
        reader = csv.reader(input_file, delimiter="\t")

        targets = []

        for row in reader:
            targets.append(DownloadTarget(*row))

    return targets
