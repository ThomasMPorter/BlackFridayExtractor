import configparser
import unittest

import tmpimgur

#----------------------------
# Set to your cfg file
cfg_file = 'src/local.cfg'
#----------------------------

class testConnection(unittest.TestCase):

    def test_upload_image(self):
        # Arrange
        album = get_test_album()
        image_url = config['unittest']['test_image_url']

        # Act
        actual = album.upload_image(image_url)

        # Assert
        self.assertIsNotNone(actual)


config = configparser.ConfigParser()
config.read(cfg_file)

def get_test_connection():
    return tmpimgur.Connection(
        config['unittest']['test_url'],
        config['unittest']['test_client_id'])


def get_test_album():
    result = get_test_connection().get_album(config['unittest']['exist_album_id'])
    result.set_album_deletehash(config['unittest']['exist_album_deletehash'])
    return result


if __name__ == '__main__':
    unittest.main()
