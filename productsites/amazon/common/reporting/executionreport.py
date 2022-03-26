class ExecutionReport:

    def __init__(self, leaf_stats, file_path, crawler=None):
        self.leaf_stats = leaf_stats
        self.crawler = crawler
        self.file_path = file_path

    def add_leaf(self, leaf):
        leaf_id = self.extract_leaf_id(leaf)
        self.leaf_stats[leaf_id] = dict()
        self.leaf_stats[leaf_id]['url'] = leaf
        self.leaf_stats[leaf_id]['count'] = 0

    def increment_leaf_product_count(self, url, count):
        leaf_id = self.extract_leaf_id(url)
        self.leaf_stats[leaf_id]['count'] = self.leaf_stats[leaf_id]['count'] + count

    @staticmethod
    def add_error(crawler, error_type, error_msg):
        errors = crawler.stats.get_value(error_type)
        if not errors:
            errors = []
        errors.append(error_msg + '\n')
        crawler.stats.set_value(error_type, errors)

    @staticmethod
    def extract_leaf_id(url):
        index = str(url).find("/ref=zg_b")
        if index > 0:
            url = str(url)[0:index]

        index = str(url).rfind('/')
        leaf_id = url[index + 1:]
        return leaf_id

    def build_execution_report(self, crawler):
        self.crawler = crawler
        file = open(
            self.file_path + '_' + str(self.crawler.stats.get_value('start_time')).replace('-', '_').replace(':',
                                                                                                             '_').replace(
                ' ', '') + '.txt', 'w')
        product_count = 0
        file.write('################ REPORT #################################\n')
        file.write("start time: " + str(self.crawler.stats.get_value('start_time')) + '\n')
        file.write("end time: " + str(self.crawler.stats.get_value('finish_time')) + '\n')

        for k, v in self.leaf_stats.items():
            file.write(str(v['url']) + " : " + str(v['count']) + '\n')
            product_count += v['count']
        file.write("leaves with no products count: " + str(self.crawler.stats.get_value('leaves_no_product_count')) + '\n')
        file.write("total number of products found:" + str(product_count) + '\n')
        file.write(
            "item scraped count: " + str(self.crawler.stats.get_value('item_scraped_count')) + '\n')
        file.write(
            "elapsed time seconds: " + str(self.crawler.stats.get_value('elapsed_time_seconds')) + '\n')

        file.write("DB_error_count: " + str(self.crawler.stats.get_value('DB_error_count')) + '\n')

        file.write("new product table records added to DB: " + str(
            self.crawler.stats.get_value('new_product_DB_count')) + '\n')
        file.write(
            "expired products added to DB: " + str(self.crawler.stats.get_value('expired_products_DB_count')) + '\n')
        file.write("new scoring DB: " + str(self.crawler.stats.get_value('new_scoring_DB_count')) + '\n')
        file.write("new_snapshot_DB_count: " + str(self.crawler.stats.get_value('new_snapshot_DB_count')) + '\n')
        file.write(
            "existing product found in DB: " + str(self.crawler.stats.get_value('existing_product_count')) + '\n')
        errors = self.crawler.stats.get_value('DB_error_msgs')
        counter = 1
        if errors:
            for error in errors:
                file.write('#####  ' + str(counter) + '  #####' + '\n')
                file.write(error)
                counter += 1
            file.write('#################################################')
        file.close()

    def build_execution_report_for_scheduler(self, crawler):
        self.crawler = crawler
        file = open(
            self.file_path + '_' + str(self.crawler.stats.get_value('start_time')).replace('-', '_').replace(':',
                                                                                                             '_').replace(
                ' ', '') + '.txt', 'w')
        product_count = 0
        file.write('################ REPORT #################################\n')
        file.write("start time: " + str(self.crawler.stats.get_value('start_time')) + '\n')
        file.write("end time: " + str(self.crawler.stats.get_value('finish_time')) + '\n')
        file.write("Number of products in DB that are supposed to be scraped: " + str(self.crawler.stats.get_value('urls_supposed_to_scrap_count')) + '\n')
        file.write("Number of products scraped successfully:" + str(self.crawler.stats.get_value('processed_products_count')) + '\n')
        file.write("Number of products Failed:" + str(self.crawler.stats.get_value('urls_failed_count')) + '\n')
        file.write("item scraped count: " + str(self.crawler.stats.get_value('item_scraped_count')) + '\n')
        file.write("elapsed time seconds: " + str(self.crawler.stats.get_value('elapsed_time_seconds')) + '\n')
        file.write("DB error when extracting products from scoring collection: " + str(self.crawler.stats.get_value('DB_error_when_extracting_products_to_be_scraped'))+ '\n')
        file.write("DB_error_updating_scoring_count: " + str(self.crawler.stats.get_value('DB_error_updating_scoring_count')) + '\n')
        file.write("DB_error_updating_snapshot_count: " + str(self.crawler.stats.get_value('DB_error_updating_snapshot_count')) + '\n')
        errors = self.crawler.stats.get_value('DB_error_msgs')
        counter = 1
        if errors:
            for error in errors:
                file.write('#####  ' + str(counter) + '  #####' + '\n')
                file.write(error)
                counter += 1
            file.write('#################################################')
        file.close()
