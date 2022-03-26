# Extract Product Manufacturer
# Manufacturer : WHUANZ
# Manufacturer TUANTUAN
#  but should not handle this: 'Manufacturer reference CLHRTT-K000-SM'

class Manufacturer:

    @staticmethod
    def get_manufacturer_name(product_details):
        keywords_tbl = 'Manufacturer'
        exclude_str = 'Manufacturer reference'
        exclude_str2 = 'Manufacturer part number'
        manufacturer_name = None
        table_block_str = None

        for elem in product_details:
            if keywords_tbl in elem:
                if (exclude_str not in elem) and (exclude_str2 not in elem):
                    table_block_str = elem
        if table_block_str:
            start_pos = table_block_str.find(keywords_tbl)
            if start_pos != -1:
                start_pos = start_pos + len(keywords_tbl) + 1
                manufacturer_name = table_block_str[start_pos:]
                if ":" in manufacturer_name:
                    manufacturer_name = manufacturer_name.replace(":", "")
                manufacturer_name = manufacturer_name.strip()
        return manufacturer_name

