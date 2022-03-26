# Get the "Date First Available"
# Check the existance of product ASIN in database
#       THEN
# based on the rule specified by method "can_spider_crawl_this_product()"
# Decide either to scrap (TRUE returned) the page or Not

from ...common.dao.dao import Dao as dao
from ...common.config import readconfigparameters as rd
import datetime


class ScrapingRules:
    def __init__(self):
        pass

    @staticmethod
    def get_product_number_from_url(url):
        str1 = url.split('/dp/')
        str2 = str1[1].split('/')
        prod_id = str2[0]
        return prod_id[0:10]

    @staticmethod
    def get_product_number_from_url_reviews(url):
        str1 = url.split('/product-reviews/')
        str2 = str1[1].split('/')
        prod_id = str2[0]
        return prod_id[0:10]

    @staticmethod
    def is_product_in_db(url):
        prod_id = ScrapingRules.get_product_number_from_url(url)
        return dao.find_product(prod_id)

    @staticmethod
    def is_expired_product(item):
        d1 = datetime.datetime.now().date()
        dfa = item['date_first_available']

        if dfa:
            if "." in item['date_first_available']:
                d0 = datetime.datetime.strptime(dfa, "%b. %d %Y").date()
            else:
                try:
                    d0 = datetime.datetime.strptime(dfa, "%b %d %Y").date()
                except Exception as ex:
                    d0 = datetime.datetime.strptime(dfa, "%B %d %Y").date()
            if (d1 - d0).days <= int(rd.expiration_in_days):
                return False
            else:
                return True
        else:
            return True

    # used to update product: to add description, images and reviews
    @staticmethod
    def is_product_to_be_updated(item):
        return dao.is_product_to_update(item)
