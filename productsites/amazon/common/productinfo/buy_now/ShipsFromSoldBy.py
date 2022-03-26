# types of phrases in this section include:
# phrase 1:
# Ships from and sold by Amazon.ca.
# phrase 2
# Sold by ROC-PENG and Fulfilled by Amazon.
# phrase 3
# Ships from Canada and sold by eShine Car Care.
# phrase 4
# to add new case if any

class ProductShipsFromSoldBy:
    @staticmethod
    def get_product_ships_from_sold_by(buy_now):
        sold_by_amazon = 'Ships from and sold by'
        starts_with_sold_by = 'Sold by'
        fulfilled_by = 'and Fulfilled by'
        starts_with_ships_from = 'Ships from'
        and_sold_by = 'and sold by '

        ships_from_sold_by = {'ships_from': None, 'sold_by': None}
        product_ships_from = None
        product_sold_by = None

        if buy_now['ships_from_soldby']:
            # handles phrase 1 case
            if sold_by_amazon in buy_now['ships_from_soldby']:
                product_ships_from = 'Amazon'
                product_sold_by = 'Amazon'
            # handles phrase 2 case
            elif ((buy_now['ships_from_soldby'].startswith(starts_with_sold_by)) and (
                    fulfilled_by in buy_now['ships_from_soldby'])):
                product_ships_from = 'Amazon'
                start_pos = buy_now['ships_from_soldby'].find(starts_with_sold_by)
                if start_pos != -1:
                    start_pos = start_pos + len(starts_with_sold_by) + 1
                end_pos = buy_now['ships_from_soldby'].find(fulfilled_by, start_pos)
                if end_pos != -1:
                    product_sold_by = buy_now['ships_from_soldby'][start_pos:end_pos]
                else:
                    product_sold_by = None
            # handles phrase 3 case
            # Ships from Canada and sold by eShine Car Care.
            elif buy_now['ships_from_soldby'].startswith(starts_with_ships_from):
                start_pos = buy_now['ships_from_soldby'].find(starts_with_ships_from)
                if start_pos != -1:
                    start_pos = start_pos + len(starts_with_ships_from) + 1
                end_pos = buy_now['ships_from_soldby'].find(and_sold_by, start_pos)
                if end_pos != -1:
                    product_ships_from = buy_now['ships_from_soldby'][start_pos:end_pos]
                else:
                    product_ships_from = None
                start_pos = end_pos + len(and_sold_by)
                end_pos = buy_now['ships_from_soldby'].find('.', start_pos)
                if end_pos != -1:
                    product_sold_by = buy_now['ships_from_soldby'][start_pos:end_pos]
                else:
                    product_sold_by = None
            else:
                product_ships_from = None
                product_sold_by = None
        else:
            product_ships_from = 'New ships_from selector in Buy Now to be included in selector file'
        if product_ships_from:
            ships_from_sold_by['ships_from'] = product_ships_from.strip()
        else:
            ships_from_sold_by['ships_from'] = product_ships_from
        if product_sold_by:
            ships_from_sold_by['sold_by'] = product_sold_by.strip()
        else:
            ships_from_sold_by['sold_by'] = product_sold_by

        return ships_from_sold_by
