from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings, get_config
import os



os.environ.setdefault('SCRAPY_PROJECT', 'default')
conf = get_config()
process = CrawlerProcess(get_project_settings())

process.crawl('amazon_spider', file='amazon/test/testamz.txt', country='ca')
#process.crawl('amazon_scheduler', file='amazon/test/leaves/amzca4.txt', country='ca')

process.start()
