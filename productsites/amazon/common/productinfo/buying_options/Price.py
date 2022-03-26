import logging

logger = logging.getLogger()


class Price:
    @staticmethod
    def get_product_price(buying_options):
        try:
            if buying_options['price_whole1']:
                price_symbol = buying_options['price_symbol1']  #price_symbol = '$'
                price_whole = buying_options['price_whole1']
                price_whole_cleaned = price_whole.strip('.').strip()
                price_fraction = buying_options['price_fraction1']
                product_price = str(price_whole_cleaned) + '.' + str(price_fraction.strip())
                return product_price
        except KeyError as ke:
            pass
        logger.error('New product price selector in Buying Options not included')
        return ''
