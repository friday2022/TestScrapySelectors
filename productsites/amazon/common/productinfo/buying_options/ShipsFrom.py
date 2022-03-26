import logging

logger = logging.getLogger()


class ShipsFrom:
    @staticmethod
    def get_product_ships_from(buying_options):
        ships_from = None
        try:
            if buying_options['ships_from1']:
                ships_from = buying_options['ships_from1']
        except KeyError as ke:
            pass

        if not ships_from:
            try:
                if buying_options['ships_from2']:
                    ships_from = buying_options['ships_from2']
            except KeyError as ke:
                pass

        if ships_from:
            sf_str1 = ships_from.split('from')
            sf_str2 = sf_str1[1].split('.')
            product_ships_from = sf_str2[0].strip()
            return product_ships_from
        else:
            logger.error('New ships_from selector in Buying Options to be included in selector file')
        return ''
