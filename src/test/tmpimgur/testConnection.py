import configparser
import unittest

import tmpimgur

#----------------------------
# Set to your cfg file
cfg_file = 'src/local.cfg'
#----------------------------

class testConnection(unittest.TestCase):

    def test_create_album(self):

        # Arrange
        connection = get_test_connection()
        album_title = config['unittest']['create_album_title']

        # Act
        album = connection.create_album(album_title)

        actual = None

        if album:
            actual = album.album_id

        # Assert
        self.assertIsNotNone(actual)

    def test_get_album(self):

        # Arrange
        connection = get_test_connection()
        album_id = config['unittest']['exist_album_id']
        expected = config['unittest']['exist_album_title']

        # Act
        album = connection.get_album(album_id)

        actual = None

        if album:
            actual = album.album_title

        # Assert
        self.assertEqual(expected, actual)

config = configparser.ConfigParser()
config.read(cfg_file)

def get_test_connection():
    return tmpimgur.Connection(
        config['unittest']['test_url'], 
        config['unittest']['test_client_id'])

if __name__ == '__main__':
    unittest.main()
