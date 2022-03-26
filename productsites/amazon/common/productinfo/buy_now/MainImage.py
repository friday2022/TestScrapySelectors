import logging

logger = logging.getLogger()


class MainImage:
    @staticmethod
    def get_product_main_image(buy_now):

        try:
            if buy_now['main_image_link1']:
                return buy_now['main_image_link1']
        except KeyError as ke:
            pass

        logger.error('New product Main Image selector in Buy Now to be included')
        return ''