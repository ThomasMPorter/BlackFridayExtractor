
import requests
from bs4 import BeautifulSoup


class ExtractGottadeal:
    """"""

    def __init__(
            self,
            store_name: str):
        """"""
        self.store_name = store_name

    def get_image_url_list(
            self,
            page_start: int,
            page_end: int):
        """Get the list of Images from gottadeal.com"""

        image_url_list = []

        page = page_start

        next_button_exists = True

        while next_button_exists:

            url = 'https://blackfriday.gottadeal.com/BlackFridayScans/{}/{}'.format(
                self.store_name,
                page)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

            result = requests.get(url, headers=headers)

            soup = BeautifulSoup(result.text, 'html.parser')

            div = soup.find('div', attrs={'class': 'wide_card_scan_pages'})

            img = div.find('img')

            image_url_list.append(img['src'])

            if page_end and page == page_end:
                break

            page += 1

            next_button_exists = soup.find('a', text='Next')

        return image_url_list
