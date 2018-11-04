import cssutils
import requests
from bs4 import BeautifulSoup

class ExtractBfads:
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
        """Get the list of Images"""

        image_url_list = []
        album_title = None

        page = page_start

        next_button_exists = True

        while next_button_exists:

            url = 'https://www.bfads.net/stores/{}/ads/{}/page-{}'.format(
                self.store_name,
                self.type_of_ad,
                page)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

            result = requests.get(url, headers=headers)

            soup = BeautifulSoup(result.text, 'html.parser')

            if not album_title: 
                title_h1 = soup.find('h1', attrs={'class': 'heading-store'})
                album_title = title_h1.find(text=True)

            image_url_found = False

            for styles in soup.select('style'):

                if image_url_found:
                    break

                for rule in cssutils.parseString(styles.encode_contents()):
                    if (rule.type == rule.STYLE_RULE
                            and rule.selectorText == "#AdscanPage{}".format(page)):
                        s = rule.style.background
                        image_url_list.append(s[s.find("(")+1:s.find(")")])
                        image_url_found = True
                        break

            if page_end and page == page_end:
                break

            page += 1

            next_button_exists = soup.find('a', attrs={'class': 'next'})

        return image_url_list, album_title
