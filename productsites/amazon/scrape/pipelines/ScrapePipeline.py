# Define your item pipelines here
#
# Don't forget to add your pipelines to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from ...common.dao.dao import Dao
from ..scrapingrules import ScrapingRules as rul


class ScrapePipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        if spider.name == 'amazon_spider':
            try:
                if item['status'] is not None and item['status'] == 'EX':
                    Dao(spider).insert_expired_product(item)
                    return item
            except KeyError as e:
                pass
            if Dao(spider).insert_product(item):
                Dao(spider).insert_scoring(item)
                Dao(spider).insert_snapshot(item)

        elif spider.name == 'amazon_scheduler':
            if rul.ScrapingRules.is_product_to_be_updated(item):
                Dao(spider).update_product(item)
                Dao(spider).set_ext_display_info(item)
            else:
                Dao(spider).update_scoring(item)
                Dao(spider).update_snapshot(item)

        return item
