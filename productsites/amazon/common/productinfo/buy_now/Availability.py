# Extract The product availability
import logging

logger = logging.getLogger()


class Availability:
    # The status of the product either: In stock , Unavailable, ....
    @staticmethod
    def get_product_availability(buy_now):
        in_stock = 'stock'
        unavailable = 'unavailable'
        try:
            if buy_now['price1'] or buy_now['price2'] or buy_now['price3']:
                return 'In stock'
            elif buy_now['availability1']:
                if in_stock in buy_now['availability1']:
                    return 'In stock'
                elif unavailable in buy_now['availability1']:
                    return 'Unavailable'
                else:
                    return buy_now['availability1']
            elif buy_now['availability2']:
                if in_stock in buy_now['availability2']:
                    return 'In stock'
                elif unavailable in buy_now['availability2']:
                    return 'Unavailable'
                else:
                    return buy_now['availability2']
        except KeyError as ke:
            pass

        logger.error('New availability selector for BuyNow')
        return ''
