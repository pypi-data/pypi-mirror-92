""" Test for downloader functionalities. """


import logging

from src.tdownloader.input_file_reader import read_file

logger = logging.getLogger("File tests")
logger.setLevel(logging.DEBUG)


class TestFileRelated:

    def test_read_file(self, input_file):
        logger.debug(input_file)

        result = read_file(input_file)

        assert len(result) == 10
        assert result[0].file_name == "BreakingBadS2.part011.rar"
        assert result[0].url == "https://s3.todus.cu/todus/file/2021-01-26/a56/" \
                                "a56ac378ef15eaee3bc50fb7c852d061b8361cba10e8f7dde51fd74f9b71d19b"

