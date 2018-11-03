"""Imgur Album Object"""
import requests

import tmpimgur


class Album:
    """Imgur Album Object"""

    def __init__(
            self,
            connection: tmpimgur.Connection,
            album_id: str,
            album_deletehash: str,
            album_title):
        """Imgur Album Object init"""

        if not connection:
            raise ValueError('connection cannot be None')

        if not album_id:
            raise ValueError('album_id cannot be None')

        if not album_title:
            raise ValueError('album_title cannot be None')

        self.connection = connection
        self.album_id = album_id
        self.album_deletehash = album_deletehash
        self.album_title = album_title

        self.server_url = connection.server_url
        self.client_id = connection.client_id
        self.album_url = 'https://imgur.com/a/{}'.format(album_id)

    def set_album_deletehash(self, album_deletehash):
        """"""
        self.album_deletehash = album_deletehash

    def upload_image(self, image_url: str):
        """Upload image to this album from image_url. Returns image_id"""

        url = "{}/3/image".format(self.server_url)

        payload = (
            '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n'
            'Content-Disposition: form-data; name="image"\r\n\r\n'
            '{}\r\n'
            '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n'
            'Content-Disposition: form-data; name="album"\r\n\r\n'
            '{}\r\n'
            '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n'
            'Content-Disposition: form-data; name="type"\r\n\r\n'
            'URL\r\n'
            '------WebKitFormBoundary7MA4YWxkTrZu0gW--'.format(
                image_url,
                self.album_deletehash))

        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Authorization': "Client-ID {}".format(self.client_id)}

        response = requests.request("POST", url, data=payload, headers=headers)
        response.raise_for_status

        json_data = response.json()

        if not json_data:
            return None

        if "error" in json_data["data"]:
            raise ValueError(json_data["data"]["error"])

        return json_data["data"]["id"]

    def update_title(self, new_title: str):

        url = "{}/3/album/{}".format(self.server_url, self.album_deletehash)

        payload = (
            '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n'
            'Content-Disposition: form-data; name="title"\r\n\r\n'
            '{}\r\n' 
            '------WebKitFormBoundary7MA4YWxkTrZu0gW--'.format(
                new_title))

        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Authorization': "Client-ID {}".format(self.client_id)}

        response = requests.request("PUT", url, data=payload, headers=headers)
        response.raise_for_status

        json_data = response.json()
        
        if not json_data:
            return None

        if not json_data['success'] and "error" in json_data["data"]:
            raise ValueError(json_data["data"]["error"]["message"])

        self.album_title = new_title

