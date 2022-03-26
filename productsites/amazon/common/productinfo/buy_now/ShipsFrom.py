import logging

logger = logging.getLogger()


class ShipsFrom:
    @staticmethod
    def get_product_ships_from(buy_now):
        try:
            if buy_now['ships_from1']:
                return buy_now['ships_from1']
        except KeyError as ke:
            pass

        logger.error('New ships_from selector in Buy Now to be included in selector file')
        return ''
