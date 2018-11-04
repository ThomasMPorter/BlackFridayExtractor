import configparser
import unittest

import tmpbfextract

#----------------------------
# Set to your cfg file
cfg_file = 'src/local.cfg'
#----------------------------


class testExtractBfads(unittest.TestCase):

    def test_get_image_url_list(self):
        # Arrange
        extract = get_test_extract()
        page_start = 1
        page_end = 0

        # Act
        actual, _ = extract.get_image_url_list(page_start, page_end)

        # Assert
        self.assertIsNotNone(actual)


config = configparser.ConfigParser()
config.read(cfg_file)


def get_test_extract():
    return tmpbfextract.ExtractBfads(
        config['unittest']['test_bfads_store_name'],
        config['unittest']['test_bfads_type_of_ad'])


if __name__ == '__main__':
    unittest.main()
