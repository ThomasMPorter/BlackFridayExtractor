
import requests
from bs4 import BeautifulSoup


class ExtractBlackfriday:
    """"""

    def __init__(
            self,
            store_name: str, 
            type_of_ad: str):
        """"""
        self.store_name = store_name
        self.type_of_ad = type_of_ad

    def get_image_url_list(
            self,
            page_start: int,
            page_end: int):
        """Get the list of Images from Blackfriday.com"""

        image_url_list = []
        album_title = None

        page = page_start

        next_button_exists = True

        while next_button_exists:

            url = 'https://blackfriday.com/ads/{}/{}/{}'.format(
                self.type_of_ad,
                self.store_name,
                page)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

            result = requests.get(url, headers=headers)

            soup = BeautifulSoup(result.text, 'html.parser')

            if not album_title:
                title_div = soup.find('div', attrs={'class': 'pure-u-1'}) 
                album_title = title_div.find('h1').find(text=True)

            print_ad = soup.find('print-ad')

            image_url_list.append(print_ad['image-url'])

            if page_end and page == page_end:
                break

            page += 1

            next_button = soup.find('i', attrs={'class': 'fa fa-angle-right'})

            next_button_exists = (next_button.parent.name == 'a')

        return image_url_list, album_title
