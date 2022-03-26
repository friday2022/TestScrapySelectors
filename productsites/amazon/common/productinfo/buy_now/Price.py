import logging

logger = logging.getLogger()


class Price:
    @staticmethod
    def get_product_price(buy_now):

        try:
            if buy_now['price1']:
                return buy_now['price1'][1:]
        except KeyError as ke:
            pass
        try:
            if buy_now['price2']:
                return buy_now['price2'][1:]
        except KeyError as ke:
            pass
        try:
            if buy_now['price3']:
                return buy_now['price3'][1:]
        except KeyError as ke:
            pass

        logger.error('New product price selector in Buy Now to be included in selector file')
        return ''
