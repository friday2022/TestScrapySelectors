# extract product Number

class ProductNumber:

    @staticmethod
    def get_product_number(product_details_list):
        product_number = None
        # in case of scrapper, product number = asin
        keywords_tbl = 'ASIN'
        table_block_str = None

        for elem in product_details_list:
            if keywords_tbl in elem:
                table_block_str = elem
        if table_block_str:
            start_pos = table_block_str.find(keywords_tbl)
            if start_pos != -1:
                start_pos = start_pos + len(keywords_tbl) + 1
                product_number = table_block_str[start_pos:]
                if ":" in product_number:
                    product_number = product_number.replace(":", "")
                product_number = product_number.strip()
        return product_number[0:10]
