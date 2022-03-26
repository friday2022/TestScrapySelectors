import logging
from bs4 import BeautifulSoup

logger = logging.getLogger()


class ImagesLinks:
    @staticmethod
    def get_product_images_links(buy_now):

        try:
            if buy_now['images_links_vertical']:
                return ImagesLinks.get_images_from_HTML(buy_now['images_links_vertical'])
            elif buy_now['images_links_horizontal']:
                return ImagesLinks.get_images_from_HTML(buy_now['images_links_horizontal'])
        except KeyError as ke:
            pass

        logger.error('New product Images linksselector in Buy Now to be included')
        return ''

    @staticmethod
    def get_images_from_HTML (html_list):
        html_str = ' '
        images_list_links = []
        for str in html_list:
            html_str += str
        soup = BeautifulSoup(html_str, 'html.parser')
        el = soup.find_all('img')
        for each_e in el:
            images_list_links.append(each_e.get('src'))
        del images_list_links[-1]
        if images_list_links:
            return images_list_links
        else:
            return None
