import configparser
import unittest

import tmpbfextract

#----------------------------
# Set to your cfg file
cfg_file = 'src/local.cfg'
#----------------------------


class testExtractGottadeal(unittest.TestCase):

    def test_get_image_url_list(self):
        # Arrange
        extract = get_test_extract_bfads()
        page_start = 1
        page_end = 0

        # Act
        actual = extract.get_image_url_list(page_start, page_end)

        # Assert
        self.assertIsNotNone(actual)


config = configparser.ConfigParser()
config.read(cfg_file)


def get_test_extract_bfads():
    return tmpbfextract.ExtractGottadeal(
        config['unittest']['test_gottadeal_store_name'])


if __name__ == '__main__':
    unittest.main()
