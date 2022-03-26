import logging

logger = logging.getLogger()


class ShippingPrice:
    @staticmethod
    def get_product_shipping_price(buy_now):
        free_shipping = 'FREE'
        delivery = 'delivery'

        try:
            if buy_now['shipping_price2']:
                if free_shipping in buy_now['shipping_price2']:
                    return 0
                # handle the following: '$5.54 delivery March 4 - 24. Details'
                elif delivery in buy_now['shipping_price2']:
                    return buy_now['shipping_price2'].split()[0][1:]
                else:
                    return buy_now['shipping_price2'][1:]
            elif buy_now['shipping_price1']:
                return buy_now['shipping_price1'][1:]
        except KeyError as ke:
            pass

        logger.error('New shipping price selector in Buy Now to be included in selector file')
        return ''
