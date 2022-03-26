# extract product category score directly from BSR - specific to scrapper

class CategoryScore:
    @staticmethod
    def get_category_score(best_seller_rank):
        try:
            if best_seller_rank['category_sub4']:
                return best_seller_rank['category_sub4_rank']
        except KeyError as ke:
            pass

        try:
            if best_seller_rank['sub_sub_category']:
                return best_seller_rank['sub_sub_category_rank']
        except KeyError as ke:
            pass

        try:
            if best_seller_rank['sub_category']:
                return best_seller_rank['sub_category_rank']
        except KeyError as ke:
            pass

        try:
            if best_seller_rank['category']:
                return best_seller_rank['category_rank']
        except KeyError as ke:
            pass

        return None