# Extract Product ISBN.
# some products have only ISBN instead of ASIN


class ISBN:

    @staticmethod
    def get_product_isbn(product_details_list):
        product_isbn = None
        keywords_tbl = 'ISBN'
        table_block_str = None

        for elem in product_details_list:
            if keywords_tbl in elem:
                table_block_str = elem
        if table_block_str:
            start_pos = table_block_str.find(keywords_tbl)
            if start_pos != -1:
                start_pos = start_pos + len(keywords_tbl) + 1
                product_isbn = table_block_str[start_pos:]
                if ":" in product_isbn:
                    product_isbn = product_isbn.replace(":", "")
                product_isbn = product_isbn.strip()
        return product_isbn
