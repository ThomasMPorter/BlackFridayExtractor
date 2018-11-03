""""""
import requests

import tmpimgur


class Connection:
    """"""

    def __init__(self, server_url: str, client_id: str):
        """"""
        self.server_url = server_url
        self.client_id = client_id

    def create_album(self, album_title: str):
        """"""

        url = "{}/3/album".format(self.server_url)

        payload = (
            '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n'
            'Content-Disposition: form-data; name="title"\r\n\r\n'
            '{}\r\n'
            '------WebKitFormBoundary7MA4YWxkTrZu0gW--').format(
                album_title)

        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Authorization': "Client-ID {}".format(self.client_id)}

        response = requests.request("POST", url, data=payload, headers=headers)
        response.raise_for_status

        json_data = response.json()

        if not json_data:
            return None

        if "error" in json_data["data"]:
            raise ValueError(json_data["data"]["error"]["message"])

        return tmpimgur.Album(
            self,
            json_data["data"]["id"],
            json_data["data"]["deletehash"],
            album_title)

    def get_album(self, album_id: str):

        url = "{}/3/album/{}".format(self.server_url, album_id)

        headers = {'Authorization': 'Client-ID {}'.format(self.client_id)}

        response = requests.request("GET", url, headers=headers)
        response.raise_for_status

        json_data = response.json()
        
        if not json_data:
            return None

        if "error" in json_data["data"]:
            raise ValueError(json_data["data"]["error"]["message"])

        return tmpimgur.Album(
            self,
            json_data["data"]['id'],
            None,
            json_data["data"]['title'])
