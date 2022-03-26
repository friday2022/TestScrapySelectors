# Extract : Product Information
# The following fields will be extracted:
# customer_reviews : number of reviews
# Parcel Dimensions or Product Dimensions with:
# product_length
# product_width
# product_height
# product_dimensions_unit
# product_weight
# product_weight_unit
# product_ASIN  OR product_ISBN (If ASIN is not available)
# product_brand
# date_first_available
# best_sellers_rank

from .buy_now import ShippingPrice as sp
from .buy_now import Price as pr
from .buy_now import Availability as avb
from .buy_now import ShipsFromSoldBy as sfsb
from .buy_now import ArrivalDate as ad
from .buy_now import Description as de
from .buy_now import MainImage as mi
from .buy_now import ImagesLinks as il




class BuyNow:

    @staticmethod
    def product_buy_now(product, buy_now_data):
        product['product_availability'] = avb.Availability.get_product_availability(buy_now_data)

        product['description'] = de.Description.get_product_description(buy_now_data)
        product['main_image_link'] = mi.MainImage.get_product_main_image(buy_now_data)
        product['images_links'] = il.ImagesLinks.get_product_images_links(buy_now_data)
        if product['product_availability'] == 'Unavailable':
            product['price'] = ''
            product['shipping_price'] = ''
            product['arrives_date'] = ''
            product['shipsfrom_soldby'] = ''
        else:
            product['price'] = pr.Price.get_product_price(buy_now_data)
            product['shipping_price'] = sp.ShippingPrice.get_product_shipping_price(buy_now_data)
            product['arrives_date'] = ad.ArrivalDate.get_product_arrival_date(buy_now_data)
            product['shipsfrom_soldby'] = sfsb.ProductShipsFromSoldBy.get_product_ships_from_sold_by(buy_now_data)


    @staticmethod
    def used_for_test_only(product, buy_now_data):
        # print in file
        f = open('buynowtest.txt', 'a')
        f.write('\n\n\n -- This is new Item:\n')
        f.write('\nProduct URL = ')
        f.write(product['product_url'])
        f.write('\nProduct ASIN = ')
        f.write(product['product_ASIN'])
        f.write('\nprice1 = ')
        if buy_now_data['price1']:
            f.write(buy_now_data['price1'])
        f.write('\nprice2 = ')
        if buy_now_data['price2']:
            f.write(buy_now_data['price2'])
        f.write('\n\n')
        f.write('\nshipping price 1 = ')
        if buy_now_data['shipping_price1']:
            f.write(buy_now_data['shipping_price1'])
        f.write('\n\n')
        f.write('\navailability1 = ')
        if buy_now_data['availability1']:
            f.write(buy_now_data['availability1'])
        f.write('\navailability2 = ')
        if buy_now_data['availability2']:
            f.write(buy_now_data['availability2'])
        f.write('\n\n')
        f.write('\narrives date 1 = ')
        if buy_now_data['arrives_date1']:
            f.write(buy_now_data['arrives_date1'])
        f.write('\n\n')
        f.write('\nships from 1 = ')
        if buy_now_data['ships_from1']:
            f.write(buy_now_data['ships_from1'])
        f.write('\n\n')
        f.write('\nsold by 1 = ')
        if buy_now_data['soldby1']:
            f.write(buy_now_data['soldby1'])

        f.write('\n\n\n -- END Item')

        f.close()
