import logging

logger = logging.getLogger()


class ShippingPrice:
    @staticmethod
    def get_product_shipping_price(buying_options):
        free_shipping = 'FREE'

        try:
            if buying_options['shipping_price2']:
                if free_shipping in buying_options['shipping_price2']:
                    return 0
                else:
                    return buying_options['shipping_price2'][1:]
            elif buying_options['shipping_price1']:
                return buying_options['shipping_price1'].split()[0][1:]
        except KeyError as ke:
            pass
        logger.error('New shipping price selector in Buying Options to be included in selector file')
        return ''
