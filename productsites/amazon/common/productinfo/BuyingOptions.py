from .buying_options import SoldBy as sb
from .buying_options import ShippingPrice as sp
from .buying_options import Price as pr
from .buying_options import Availability as avb
from .buying_options import ShipsFrom as Psf
from .buying_options import ArrivalDate as ad


class BuyingOptions:

    @staticmethod
    def product_buying_options(product, buying_options):
        product['price'] = pr.Price.get_product_price(buying_options)
        product['shipping_price'] = sp.ShippingPrice.get_product_shipping_price(buying_options)
        product['product_availability'] = avb.Availability.get_product_availability(buying_options)
        product['arrives_date'] = ad.ArrivalDate.get_product_arrival_date(buying_options)
        ships_from_sold_by = {'ships_from': Psf.ShipsFrom.get_product_ships_from(buying_options),
                              'sold_by': sb.SoldBy.get_product_sold_by(buying_options)}
        product['shipsfrom_soldby'] = ships_from_sold_by


    @staticmethod
    def used_for_test_only(product, buy_now_data):
        # print in file
        f = open('buyingtest.txt', 'a')
        f.write('\n\n\n -- This is new Item:\n')
        f.write('\nProduct URL = ')
        f.write(product['product_url'])
        f.write('\nProduct ASIN = ')
        f.write(product['product_ASIN'])
        f.write('\nprice_symbol1 = ')
        if buy_now_data['price_symbol1']:
            f.write(buy_now_data['price_symbol1'])
        f.write('\nprice_whole1 = ')
        if buy_now_data['price_whole1']:
            f.write(buy_now_data['price_whole1'])
        f.write('\nprice_fraction1 = ')
        if buy_now_data['price_fraction1']:
            f.write(buy_now_data['price_fraction1'])

        f.write('\n\n')

        f.write('\nshipping price 1 = ')
        if buy_now_data['shipping_price1']:
            f.write(buy_now_data['shipping_price1'])

        f.write('\n\n')

        f.write('\narrives_date1 = ')
        if buy_now_data['arrives_date1']:
            f.write(buy_now_data['arrives_date1'])

        f.write('\n\n')

        f.write('\nships from 1 = ')
        if buy_now_data['ships_from1']:
            f.write(buy_now_data['ships_from1'])
        f.write('\nships from 2 = ')
        if buy_now_data['ships_from2']:
            f.write(buy_now_data['ships_from2'])

        f.write('\n\n')

        f.write('\nsold by 1 = ')
        if buy_now_data['soldby1']:
            f.write(buy_now_data['soldby1'])

        f.write('\n\n\n -- END Item')

        f.close()
