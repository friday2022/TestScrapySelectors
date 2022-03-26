import time

import scrapy
from ...common.reporting.executionreport import ExecutionReport
from ...common.config import readconfigparameters as rd
from selectorlib import Extractor
from scrapy.http import Request
from ..scrapingrules import ScrapingRules as rul
from ...common.productinfo import ProductCommon as pc
from ...common.productinfo import BuyNow as pbn
from ...common.productinfo import BuyingOptions as pbo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from ..scrapingrules.ScrapingRules import ScrapingRules as sr
from ...common.productinfo import Reviews as rv
import importlib.resources as pkg_resources
import logging
from ..scrapingrules.ScrapingRules import ScrapingRules

logger = logging.getLogger()
product_list_yml_prefix = rd.product_list_yml_prefix
buy_now_yml_prefix = rd.buy_now_yml_prefix
see_options_yml_prefix = rd.see_options_yml_prefix
reviews_yml_prefix = rd.reviews_yml_prefix
output_file = "amazon/test/output.txt"

class ScrapperSpider(scrapy.Spider):
    name = 'amazon_spider'
    start_urls = []
    list_of_countries = ["ca", "com", "co.uk", "au", "de", "fr"]
    # default website is scrapper.ca
    website = 'ca'
    product_list_extractor = None
    reviews_extractor = None
    buy_now_extractor = None
    see_options_extractor = None
    driver = None

    def __init__(self, file=None, country=None, **kwargs):
        super().__init__(**kwargs)
        leaf_file_name = file
        self.driver = webdriver.Chrome("C:/chromedriver_win32/chromedriver.exe")
        ex_country_str = None
        if country:
            self.website = country
            # for co.uk and com.au change dot to create the extractors.
            ex_country_str = self.website
            if "." in ex_country_str:
                ex_country_str = ex_country_str.replace(".", "_")

        if self.website in self.list_of_countries:
            # Create Extractors by reading from the YML files
            product_list_yml_file_content = pkg_resources.read_text(rd.yml_package_path,
                                                                    (product_list_yml_prefix + ex_country_str + ".yml"))
            buy_now_yml_file_content = pkg_resources.read_text(rd.yml_package_path,
                                                               (buy_now_yml_prefix + ex_country_str + ".yml"))
            see_options_yml_file_content = pkg_resources.read_text(rd.yml_package_path,
                                                                   (see_options_yml_prefix + ex_country_str + ".yml"))
            reviews_yml_file_content = pkg_resources.read_text(rd.yml_package_path,
                                                               (reviews_yml_prefix + ex_country_str + ".yml"))
            self.product_list_extractor = Extractor.from_yaml_string(product_list_yml_file_content)
            self.buy_now_extractor = Extractor.from_yaml_string(buy_now_yml_file_content)
            self.see_options_extractor = Extractor.from_yaml_string(see_options_yml_file_content)
            self.reviews_extractor = Extractor.from_yaml_string(reviews_yml_file_content)

        try:
            with open(leaf_file_name, 'r') as f:
                leaves = f.readlines()
                for leaf in leaves:
                    leaf = leaf.strip('\n')
                    self.start_urls.append(leaf)
                if self.website == "com":
                    self.start_urls = ['https://www.amazon.com/gp/new-releases/sporting-goods/ref=zg_bsnr_nav_0']
                if self.website == "co.uk":
                    self.start_urls = ['https://www.amazon.co.uk/gp/new-releases/sports/ref=zg_bsnr_nav_0']
        except Exception as e:
            print("error while reading leaves file tt" + str(e))


    def parse(self, response):
       product = dict()
       url_to_test = self.start_urls[0]
       product['product_url'] = url_to_test
       product['country_website'] = self.website
       yield Request(url_to_test, self.parse_product, meta={'product': product}, dont_filter=True)


    def parse_product(self, response):
        product = response.meta.get('product')
        data = self.buy_now_extractor.extract(response.text, base_url=response.url)
        if data['title'] is None:
            product["title"] = "Product Title is NONE"
            ScrapperSpider.print_product(product)
            return
        if data['title'] is not None:  # check if product page is not empty
            pc.ProductCommon.product_common_info(product, data)
            buying_options_url = data['see_buying_options_url']
            product['url_buying_options'] = buying_options_url
            if buying_options_url:
                product['page_layout'] = 'See All Buying Options'
                request = Request(buying_options_url, self.parse_reviews)
                request.cb_kwargs['product'] = product
                yield request
            else:
                product['page_layout'] = 'Buy Now'
                pbn.BuyNow.product_buy_now(product, data)
                reviews_url = rd.reviews_sub_url1 + self.website + rd.reviews_sub_url2 + product[
                    "product_ASIN"] + rd.reviews_sub_url3
                request = Request(reviews_url, self.parse_reviews)
                request.cb_kwargs['product'] = product
                yield request

    def parse_buying_options(self, response, product):
        #product = response.meta.get('product')
        self.wait = WebDriverWait(self.driver, poll_frequency=2, timeout=10)
        self.driver.get(response.url)
        self.scroll_until_loaded()
        html_str = self.driver.page_source
        see_options_data = self.see_options_extractor.extract(html_str)
        pbo.BuyingOptions.product_buying_options(product, see_options_data)
        reviews_url = rd.reviews_sub_url1 + self.website + rd.reviews_sub_url2 + product["product_ASIN"] + rd.reviews_sub_url3
        request = Request(reviews_url, self.parse_reviews)
        request.cb_kwargs['product'] = product
        yield request

    # This method is used by selenium
    def scroll_until_loaded(self):
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;") > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;")
            except TimeoutException:
                break

    def parse_reviews(self, response, product):
        data = self.reviews_extractor.extract(response.text, base_url=response.url)
        if data:
            if data['reviews'] is None:
                #ScrapperSpider.print_product(product)
                yield product
            if data['reviews'] is not None:
                self.product_number_from_reviews_response = None
                self.product_number_from_reviews_response = sr.get_product_number_from_url_reviews(response.url)
                reviews_list = []
                review_count = 1
                for review in data['reviews']:
                    if review_count > int(rd.max_reviews_to_scrap):
                        break
                    reviews_list.append(review.copy())
                    review_count += 1
                rv.Reviews.add_reviews_to_product_info(product, reviews_list)
                self.crawler.stats.inc_value('reviews_processed_count', 1)
                self.reviews_retry_count = 0
                #ScrapperSpider.print_product(product)
                yield product

    @staticmethod
    def print_product(product):
        try:
            with open(output_file, "w") as file:
                file.write("product_ASIN: ")
                file.write(product["product_ASIN"])
                file.write("\nproduct_url: ")
                file.write(product["product_url"])
                file.write("\ncountry_website: ")
                file.write(product["country_website"])
                file.write("\ntitle: ")
                file.write(product["title"])
                file.write("\ndescription: ")
                file.write(product["description"])
                file.write("\nmain_image_link: ")
                file.write(product["main_image_link"])
                file.write("\nimages_links: ")
                file.write(product["images_links"])
                file.write("\nprice: ")
                file.write(product["price"])
                file.write("\nshipping_price: ")
                file.write(product["shipping_price"])
                file.write("\narrives_date: ")
                file.write(product["arrives_date"])
                file.write("\nshipsfrom_soldby: ")
                file.write(product["shipsfrom_soldby"])
                file.write("\nproduct_brand: ")
                file.write(product["product_brand"])
                file.write("\nmanufacturer: ")
                file.write(product["manufacturer"])
                file.write("\nproduct_availability: ")
                file.write(product["product_availability"])
                file.write("\nbest_sellers_rank: ")
                file.write(product["best_sellers_rank"])
                file.write("\nproduct_category: ")
                file.write(product["product_category"])
                file.write("\ndate_first_available not formatted: ")
                file.write(product["date_first_available"])
                file.write("\nparcel_dimensions: ")
                file.write(product["parcel_dimensions"])
                file.write("\nproduct_ISBN: ")
                file.write(product["product_ISBN"])
                file.write("\nsellingFactor: ")
                file.write(product["sellingFactor"])
                file.write("\nanswered_questions_count: ")
                file.write(product["answered_questions_count"])
                file.write("\ncustomer_reviews: ")
                file.write(product["customer_reviews"])
                file.write("\nurl_buying_options: ")
                file.write(product["url_buying_options"])
                file.write("\npage_layout: ")
                file.write(product["page_layout"])
                file.write("\nreviews last 3 reviews: ")
                file.write(product["reviews"])
        except Exception as e:
            print("error while writing product file <" + output_file + ">" + str(e))


    def closed(self, reason):
        # will be called when the crawler process ends
        self.driver.close()
        self.driver.quit()
