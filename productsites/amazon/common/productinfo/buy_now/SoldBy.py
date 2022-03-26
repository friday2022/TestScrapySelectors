import logging

logger = logging.getLogger()


class SoldBy:
    @staticmethod
    def get_product_sold_by(buy_now):
        try:
            if buy_now['soldby1']:
                return buy_now['soldby1']
        except KeyError as ke:
            pass

        logger.error('New soldby selector in BuyNow to be included in selector file')
        return ''
