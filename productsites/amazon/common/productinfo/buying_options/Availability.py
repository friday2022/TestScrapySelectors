# Extract The product availability

import logging

logger = logging.getLogger()


class Availability:
    # The status of the product either: In stock
    @staticmethod
    def get_product_availability(buying_options):
        try:
            if buying_options['price_whole1']:
                return 'In stock'
            else:
                return 'Unavailable'
        except KeyError as ke:
            pass
        logger.error('New availability selector for Buying Options')
        return ''