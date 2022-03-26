# extract product Brand either from product details (using: product_details)
# or from product page(using item)

import logging

logger = logging.getLogger()


class Brand:
    @staticmethod
    def get_product_brand(product_details, item):
        product_brand = None
        keywords_tbl = 'Brand'
        table_block_str = None

        for elem in product_details:
            if keywords_tbl in elem:
                table_block_str = elem

        if table_block_str:
            start_pos = table_block_str.find(keywords_tbl)
            if start_pos != -1:
                start_pos = start_pos + len(keywords_tbl) + 1
                product_brand = table_block_str[start_pos:]

                if ":" in product_brand:
                    product_brand = product_brand.replace(":", "")
                product_brand = product_brand.strip()

        if product_brand is None:
            product_brand = Brand.process_brand(item)
        return product_brand

    @staticmethod
    def process_brand(item):
        product_brand = None
        keywords_tbl = 'Brand'

        try:
            table_block_str = item['brand1']
        except KeyError as ke:
            logger.error("product brand missing")

        if table_block_str:
            start_pos = table_block_str.find(keywords_tbl)
            if start_pos != -1:
                start_pos = start_pos + len(keywords_tbl) + 1
                product_brand = table_block_str[start_pos:]
                if ":" in product_brand:
                    product_brand = product_brand.replace(":", "")
                product_brand = product_brand.strip()
        return product_brand
