import importlib.resources as pkg_resources
# reads config parameters.
from configparser import ConfigParser

# reading the contents of the config file as string
file_content_str = pkg_resources.read_text('amazon.common.configparameters', 'configparameters.ini')
parser = ConfigParser()
parser.read_string(file_content_str)

# database parameters:
server_name = parser.get('amazon_Mongo_DB', 'server_name')
port_number = parser.get('amazon_Mongo_DB', 'port_number')
db_name = parser.get('amazon_Mongo_DB', 'db_name')
product_collection = parser.get('amazon_Mongo_DB', 'product_collection')
scoring_collection = parser.get('amazon_Mongo_DB', 'scoring_collection')
snapshot_collection = parser.get('amazon_Mongo_DB', 'snapshot_collection')

# will be used only with scheduler
sub_url1 = parser.get('amazon_scheduler', 'sub_url1')
sub_url2 = parser.get('amazon_scheduler', 'sub_url2')
sub_url3 = parser.get('amazon_scheduler', 'sub_url3')
reviews_sub_url1 = parser.get('amazon_scheduler', 'reviews_sub_url1')
reviews_sub_url2 = parser.get('amazon_scheduler', 'reviews_sub_url2')
reviews_sub_url3 = parser.get('amazon_scheduler', 'reviews_sub_url3')
max_reviews_retries = parser.get('amazon_scheduler', 'max_reviews_retries')
max_reviews_to_scrap = parser.get('amazon_scheduler', 'max_reviews_to_scrap')
reviews_yml_prefix = parser.get('amazon_scheduler', 'reviews_yml_prefix')
days_cycle = parser.get('amazon_scheduler', 'days_elapse_before_reschedule')
max_record_number = parser.get('amazon_scheduler', 'max_record_number')

# will be used only with scrapper
expiration_in_days = parser.get('amazon_scrapper', 'expiration_in_days')
product_list_yml_prefix = parser.get('amazon_scrapper', 'product_list_yml_prefix')
max_retry = parser.get('amazon_scrapper', 'max_retry')
scroll_pause_time = parser.get('amazon_scrapper', 'scroll_pause_time')

# will be used by both scrapper and scheduler
max_product_retries = parser.get('common', 'max_product_retries')
buy_now_yml_prefix = parser.get('common', 'buy_now_yml_prefix')
see_options_yml_prefix = parser.get('common', 'see_options_yml_prefix')
chrome_driver_path = parser.get('common', 'chrome_driver_path')
yml_package_path = parser.get('common', 'yml_package_path')
max_scraping_count = parser.get('common', 'max_scraping_count')
score_threshold = parser.get('common', 'score_threshold')