import logging
import urllib.request
import pymongo
from pymongo.errors import OperationFailure
from ..config import readconfigparameters as rd
from datetime import date, timedelta
from datetime import datetime
from ..reporting.executionreport import ExecutionReport

conn = pymongo.MongoClient(rd.server_name, int(rd.port_number))
db = conn[rd.db_name]

product_collection = db[rd.product_collection]
scoring_collection = db[rd.scoring_collection]
snapshot_collection = db[rd.snapshot_collection]
cycling_period = rd.days_cycle
score_threshold = rd.score_threshold
max_scraping_count = rd.max_scraping_count
max_record_number = rd.max_record_number  # used by dao as max records to be selected from database (for scraping)
logger = logging.getLogger()


# The pipelines in mongodb
class Dao:

    def __init__(self, spider):
        self.spider = spider
        pass

    def insert_product(self, item):
        product = Dao.get_product(item)
        logger.info('inserting product with product number=' + product['product_number'])
        try:
            product_collection.insert(dict(product))
            self.spider.crawler.stats.inc_value('new_product_DB_count', 1)
        except OperationFailure as ex:
            logger.error("exception while inserting product %s", ex)
            self.spider.crawler.stats.inc_value('DB_error_count', 1)
            ExecutionReport.add_error(self.spider.crawler, 'DB_error_msgs', 'product number in url: ' +
                                      str(item['url_product_number']) + '\n\tproduct number: '
                                      + str(product['product_number'])
                                      + '\n\t error msg:' + str(ex))
            return None
        return item

    def insert_expired_product(self, item):
        product = dict()
        product['_id'] = item['product_ASIN'] + "_" + item['country_website']
        product['status'] = item['status']
        product['country'] = item['country_website']
        product['product_number'] = item['product_ASIN']
        date_first_available_formatted = datetime.strptime(item['date_first_available'], '%b %d %Y').strftime('%Y%m%d')
        product['first_date_available'] = date_first_available_formatted
        product['first_date_scraped'] = date.today().strftime("%Y%m%d")
        logger.info('inserting product number =' + product['product_number'])
        try:
            product_collection.insert(dict(product))
            self.spider.crawler.stats.inc_value('expired_products_DB_count', 1)
        except OperationFailure as ex:
            logger.error("exception while inserting product %s", ex)
            self.spider.crawler.stats.inc_value('DB_error_count', 1)
            ExecutionReport.add_error(self.spider.crawler, 'DB_error_msgs', 'product number in url: ' +
                                      str(item['url_product_number']) + '\n\tproduct number: '
                                      + str(product['product_number'])
                                      + '\n\t error msg:' + str(ex))
            return None
        return item

    @staticmethod
    def get_product(item):
        product = dict()
        product['_id'] = item['product_ASIN'] + "_" + item['country_website']
        product['product_number'] = item['product_ASIN']
        product['url_product_number'] = item['url_product_number']
        product['country_website'] = item['country_website']
        product['url'] = item['url']
        product['title'] = item['title']
        product['category'] = item['product_category']
        product['product_dimensions'] = item['parcel_dimensions']
        if item['date_first_available']:
            date_first_available_formatted = datetime.strptime(item['date_first_available'], '%b %d %Y').strftime(
                '%Y%m%d')
        else:
            date_first_available_formatted = None
        product['first_date_available'] = date_first_available_formatted
        product['brand'] = item['product_brand']
        product['manufacturer'] = item['manufacturer']
        return product

    def insert_scoring(self, item):
        scoring = Dao.get_scoring(item)
        try:
            scoring_collection.insert(dict(scoring))
            self.spider.crawler.stats.inc_value('new_scoring_DB_count', 1)
        except OperationFailure as ex:
            logger.error("exception while inserting score %s", ex)
            self.spider.crawler.stats.inc_value('DB_error_count', 1)
            ExecutionReport.add_error(self.spider.crawler, 'DB_error_msgs', 'product number in url: ' +
                                      str(item['url_product_number']) + '\n\tproduct number: '
                                      + str(scoring['product_number'])
                                      + '\n\t error msg:' + str(ex))
            return None
        return item

    @staticmethod
    def get_scoring(item):
        scoring = dict()
        scoring['_id'] = item['product_ASIN'] + "_" + item['country_website']
        scoring['product_number'] = item['product_ASIN']
        scoring['status'] = 'IP'  # In Progress
        scoring['ext_display_info'] = False
        scoring['is_scored'] = False
        scoring['score'] = None
        scoring['scraping_counter'] = 1
        date_first_available_formatted = datetime.strptime(item['date_first_available'], '%b %d %Y').strftime('%Y%m%d')
        scoring['first_date_available'] = date_first_available_formatted
        scoring['first_date_scraped'] = date.today().strftime("%Y%m%d")
        scoring['last_date_scraped'] = date.today().strftime("%Y%m%d")
        return scoring

    def insert_snapshot(self, item):
        snapshot = Dao.get_snapshot(item)
        try:
            snapshot_collection.insert(dict(snapshot))
            self.spider.crawler.stats.inc_value('new_snapshot_DB_count', 1)
        except OperationFailure as ex:
            logger.error("exception while inserting snapshot %s", ex)
            self.spider.crawler.stats.inc_value('DB_error_count', 1)
            ExecutionReport.add_error(self.spider.crawler, 'DB_error_msgs', 'product number in url: ' +
                                      str(item['url_product_number']) + '\n\tproduct number: '
                                      + str(snapshot['product_number'])
                                      + '\n\t error msg:' + str(ex))
            return None
        return item

    @staticmethod
    def get_snapshot(item):
        snapshot = dict()
        snapshot['_id'] = item['product_ASIN'] + "_" + item['country_website']
        snapshot['product_number'] = item['product_ASIN']

        snap_list = [dict() for x in range(1)]
        snap_list[0]['date_scraped'] = date.today().strftime("%Y%m%d")
        snap_list[0]['price'] = item['price']
        snap_list[0]['shipping_price'] = item['shipping_price']
        snap_list[0]['best_sellers_rank'] = item['best_sellers_rank']
        snap_list[0]['customer_reviews'] = item['customer_reviews']
        snap_list[0]['answered_questions'] = item['answered_questions_count']
        snap_list[0]['product_availability'] = item['product_availability']
        snap_list[0]['shipsfrom_soldby'] = item['shipsfrom_soldby']
        snap_list[0]['arrives_date'] = item['arrives_date']
        snap_list[0]['review_sentiment_score'] = item['reviewSentimentScore']
        snap_list[0]['selling_factor'] = item['sellingFactor']
        snap_list[0]['page_layout'] = item['page_layout']
        snapshot['snapshot_object'] = snap_list
        return snapshot

    @staticmethod
    def find_product(product_number):
        find_query = {"$or": [{"product_number": product_number}, {"url_product_number": product_number}]}
        found = product_collection.find(find_query).count()
        if found > 0:
            return True
        else:
            return False


    # The bellow methods are used only with scheduler:
    # change: "is_scored": to True in query
    def get_products_to_scrap(self):

        today_minus7_formatted = (date.today() - timedelta(days=int(cycling_period))).strftime("%Y%m%d")
        query_condition = {"is_scored": False, "status": "IP", "last_date_scraped": {'$lt': today_minus7_formatted}}
        query_elements_to_select = {"product_number": 1}
        try:
            if scoring_collection.find(query_condition, query_elements_to_select).count() < int(max_record_number):
                products_to_scrap = scoring_collection.find(query_condition, query_elements_to_select)
            else:
                products_to_scrap = scoring_collection.find(query_condition, query_elements_to_select).sort("last_date_scraped", 1).limit(int(max_record_number))
            self.spider.crawler.stats.set_value('selected_number_of_products_to_scrap', products_to_scrap.count())
        except OperationFailure as ex:
            logger.error("exception while selecting products_to_scrap from scroring collection %s", ex)
            self.spider.crawler.stats.set_value('DB_error_when_extracting_products_to_be_scraped', 'Failed')
            ExecutionReport.add_error(self.spider.crawler, 'DB_error_msgs',
                                      'Could not extract products to scrap from scoring collection.'
                                      + '\n\t error msg:' + str(ex))
            return None
        return products_to_scrap


    @staticmethod
    def is_product_to_update(item):
        find_query = {"$and": [{"product_number": item['product_number'], "ext_display_info": True}]}
        found = scoring_collection.find(find_query).count()
        logger.error("selecting product to add description %s", item["product_number"])
        if found > 0:
            return True
        else:
            return False

    @staticmethod
    def product_has_reviews(item):
        find_query = {"$and": [{"product_number": item['product_number'], "snapshot_object.1.customer_reviews.count_reviews": {'$gt': 0}}]}
        found = snapshot_collection.find(find_query).count()
        logger.error("selecting product to add description %s", item["product_number"])
        if found > 0:
            return True
        else:
            return False

    def update_product(self, item):
        product = Dao.get_product_to_update(item)
        product_query = {"product_number": product['product_number']}
        newvalues = {"$set": {"description": product['description'], "main_image_link": product['main_image_link'], "images_links": product['images_links'], "reviews": product['reviews']} }
        try:
            product_collection.update_one(product_query, newvalues)
            self.spider.crawler.stats.inc_value('DB_success_updating_product_count', 1)
        except OperationFailure as ex:
            logger.error("exception while updating product collection %s", ex)
            self.spider.crawler.stats.inc_value('DB_error_updating_product_count', 1)
            ExecutionReport.add_error(self.spider.crawler, 'DB_error_msgs', 'product number: '
                                      + str(product['product_number'])
                                      + '\n\t error msg:' + str(ex))
            return None
        return item


    def set_ext_display_info(self, item):
        score_query = {"product_number": item['product_number']}
        newvalues = {"$set": {"ext_display_info": False}}
        try:
            scoring_collection.update_one(score_query, newvalues)
            self.spider.crawler.stats.inc_value('DB_success_updating_scoring_ext_display_info', 1)
        except OperationFailure as ex:
            logger.error("exception while updating scoring collection %s", ex)
            self.spider.crawler.stats.inc_value('DB_error_updating_scoring_ext_display_info', 1)
            ExecutionReport.add_error(self.spider.crawler, 'DB_error_msgs', 'product number: '
                                      + str(item['product_number'])
                                      + '\n\t error msg:' + str(ex))
            return None
        return item


    @staticmethod
    def get_product_to_update(item):
        product = dict()
        product['product_number'] = item['product_ASIN']
        product['description'] = item['description']
        product['main_image_link'] = item['main_image_link']
        product['images_links'] = item['images_links']
        product['reviews'] = item['reviews']
        return product

    def update_scoring(self, item):
        scoring = Dao.get_scoring_to_update(item)
        score_query = {"product_number": scoring['product_number']}
        newvalues = {"$set": {"is_scored": scoring['is_scored'], "last_date_scraped": scoring['last_date_scraped']},
                     "$inc": {"scraping_counter": 1}}
        try:
            scoring_collection.update_one(score_query, newvalues)
            self.spider.crawler.stats.inc_value('DB_success_updating_scoring_count', 1)
        except OperationFailure as ex:
            logger.error("exception while updating scoring collection %s", ex)
            self.spider.crawler.stats.inc_value('DB_error_updating_scoring_count', 1)
            ExecutionReport.add_error(self.spider.crawler, 'DB_error_msgs', 'product number: '
                                      + str(scoring['product_number'])
                                      + '\n\t error msg:' + str(ex))
            return None
        return item

    @staticmethod
    def get_scoring_to_update(item):
        scoring = dict()
        scoring['product_number'] = item['product_ASIN']
        scoring['status'] = 'IP'
        scoring['is_scored'] = False
        scoring['last_date_scraped'] = date.today().strftime("%Y%m%d")
        return scoring

    def update_snapshot(self, item):
        snapshot = Dao.get_snapshot_to_update(item)
        snap_query = {"product_number": item['product_ASIN']}
        query_push_snap = {"$push": {"snapshot_object": snapshot}}
        try:
            snapshot_collection.update(snap_query, query_push_snap)
            self.spider.crawler.stats.inc_value('DB_success_updating_snapshot_count', 1)
        except OperationFailure as ex:
            logger.error("exception while updating snapshot %s", ex)
            self.spider.crawler.stats.inc_value('DB_error_updating_snapshot_count', 1)
            ExecutionReport.add_error(self.spider.crawler, 'DB_error_msgs', 'product number: '
                                      + str(item['product_number'])
                                      + '\n\t error msg:' + str(ex))
            return None
        return item

    @staticmethod
    def get_snapshot_to_update(item):
        snap_list = dict()
        snap_list['date_scraped'] = date.today().strftime("%Y%m%d")
        snap_list['price'] = item['price']
        snap_list['shipping_price'] = item['shipping_price']
        snap_list['best_sellers_rank'] = item['best_sellers_rank']
        snap_list['customer_reviews'] = item['customer_reviews']
        snap_list['answered_questions'] = item['answered_questions_count']
        snap_list['product_availability'] = item['product_availability']
        snap_list['shipsfrom_soldby'] = item['shipsfrom_soldby']
        snap_list['arrives_date'] = item['arrives_date']
        snap_list['review_sentiment_score'] = item['reviewSentimentScore']
        snap_list['selling_factor'] = item['sellingFactor']
        snap_list['page_layout'] = item['page_layout']
        return snap_list
