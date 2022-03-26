import logging

logger = logging.getLogger()


class SoldBy:
    @staticmethod
    def get_product_sold_by(buying_options):
        try:
            if buying_options['soldby1']:
                return buying_options['soldby1']
        except KeyError as ke:
            pass

        logger.error('New soldby selector in Buying Options to be included in selector file')
        return ''
