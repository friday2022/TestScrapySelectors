# extract product category directly from BSR - specific to scrapper

class Category:
    @staticmethod
    def get_product_category(best_seller_rank):
        try:
            if best_seller_rank['category_sub4']:
                return best_seller_rank['category_sub4']
        except KeyError as ke:
            pass

        try:
            if best_seller_rank['sub_sub_category']:
                return best_seller_rank['sub_sub_category']
        except KeyError as ke:
            pass

        try:
            if best_seller_rank['sub_category']:
                return best_seller_rank['sub_category']
        except KeyError as ke:
            pass

        try:
            if best_seller_rank['category']:
                return best_seller_rank['category']
        except KeyError as ke:
            pass

        return None
