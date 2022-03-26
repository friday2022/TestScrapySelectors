# Extract Number of reviews and average score
# process the following element list:
# Customer Reviews:     4.7 out of 5 stars   57 ratings

class Reviews:

    @staticmethod
    def get_reviews_count_score(product_details, item):
        keywords_tbl = 'Customer Reviews'
        customer_reviews = {'count_reviews': None, 'reviews_score': None}
        table_block_str = None

        for elem in product_details:
            if keywords_tbl in elem:
                table_block_str = elem
        if table_block_str:
            start_pos = table_block_str.find(keywords_tbl)
            if start_pos != -1:
                start_pos = start_pos + len(keywords_tbl) + 1
                cust_rev_str = table_block_str[start_pos:]
                if ":" in cust_rev_str:
                    cust_rev_str = cust_rev_str.replace(":", "")
                cust_rev_str = cust_rev_str.strip()
                cust_rev_list = cust_rev_str.split()
                customer_reviews['count_reviews'] = cust_rev_list[5]
                customer_reviews['reviews_score'] = cust_rev_list[0]
        else:
            customer_reviews = Reviews.process_customer_reviews(item)
        return customer_reviews

    @staticmethod
    def process_customer_reviews (item):
        keywords_tbl = 'Customer Reviews'
        customer_reviews = {'count_reviews': None, 'reviews_score': None}

        table_block_str = item['customer_reviews1']
        if table_block_str:
            start_pos = table_block_str.find(keywords_tbl)
            if start_pos != -1:
                start_pos = start_pos + len(keywords_tbl) + 1
                cust_rev_str = table_block_str[start_pos:]
                if ":" in cust_rev_str:
                    cust_rev_str = cust_rev_str.replace(":", "")
                cust_rev_str = cust_rev_str.strip()
                cust_rev_list = cust_rev_str.split()
                customer_reviews['count_reviews'] = cust_rev_list[5]
                customer_reviews['reviews_score'] = cust_rev_list[0]
        return customer_reviews