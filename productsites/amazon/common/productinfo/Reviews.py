



class Reviews:

    @staticmethod
    def add_reviews_to_product_info(product, reviews_list):
        product['reviews'] = Reviews.clean_reviews_list(reviews_list)


    @staticmethod
    def clean_reviews_list(reviews):
        verified_purchase = 'Verified Purchase'

        if reviews:
            for review in reviews:
                if review['review_verified_purchase']:
                    if verified_purchase in review['review_verified_purchase']:
                        review['review_verified_purchase'] = verified_purchase
                    else:
                        review['review_verified_purchase'] = None
        return reviews
