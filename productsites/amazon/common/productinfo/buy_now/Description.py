import logging

logger = logging.getLogger()


class Description:
    @staticmethod
    def get_product_description(buy_now):

        try:
            if buy_now['description1']:
                return buy_now['description1']
        except KeyError as ke:
            pass

        logger.error('New product description selector in Buy Now to be included')
        return ''
