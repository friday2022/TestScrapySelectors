# Extract Product or Parcel Dimensions:
# strings to process are as follow:
#  Package Dimensions : 1.97 x 1.97 x 0.79 inches; 2.82 Ounces
#  Product Dimensions 35.56 x 12.7 x 5.08 cm; 1.36 Kilograms
#  Product Dimensions 23.88 x 19.3 x 3.81 cm
#  Parcel Dimensions 20 x 15 x 1 cm; 56 Grams
#  Package Dimensions : 11.42 x 2.36 x 2.36 inches
#  Product Dimensions : 11.81 x 7.87 x 3.94 inches


class Dimensions:

    @staticmethod
    def get_product_dimensions(product_details):
        dimensions_str = None
        keywords_tbl = ['Parcel Dimensions', 'Product Dimensions', 'Package Dimensions']
        table_block_str = None

        for elem in product_details:
            for i in range(len(keywords_tbl)):
                if keywords_tbl[i] in elem:
                    table_block_str = elem
        if table_block_str:
            for i in range(len(keywords_tbl)):
                start_pos = table_block_str.find(keywords_tbl[i])
                if start_pos != -1:
                    start_pos = start_pos + len(keywords_tbl[i]) + 1
                    dimensions_str = table_block_str[start_pos:]
                    if ":" in dimensions_str:
                        dimensions_str = dimensions_str.replace(":", "")
                    dimensions_str = dimensions_str.strip()

        parcel_info = dict()
        if dimensions_str:
            parcel_info['product_dimensions'] = dimensions_str
            product_dimensions_info = Dimensions.split_product_dimensions(dimensions_str)
            parcel_info['product_length'] = product_dimensions_info['product_length']
            parcel_info['product_width'] = product_dimensions_info['product_width']
            parcel_info['product_height'] = product_dimensions_info['product_height']
            parcel_info['dimension_unit'] = product_dimensions_info['product_dimensions_unit']
            parcel_info['product_weight'] = product_dimensions_info['product_weight']
            parcel_info['weight_unit'] = product_dimensions_info['product_weight_unit']
        else:
            parcel_info = None
        return parcel_info


    # handle the following str (as example)
    # '23.88 x 19.3 x 3.81 cm'
    # OR
    # '23.88 x 19.3 x 3.81 cm; 272 Grams'
    # turn it to be:
    # parcel_info['product_length'] = 23.88
    # parcel_info['product_width'] = 19.3
    # parcel_info['product_height'] = 3.81
    # parcel_info['product_dimensions_unit'] = cm
    # parcel_info['product_weight'] = 272 Or None. depends on the string to process
    # parcel_info['product_weight_unit'] = Grams or None. depends on the string to process
    @staticmethod
    def split_product_dimensions(product_dimensions):
        parcel_info = dict()
        word2 = ';'

        seq_str1 = product_dimensions.split()
        parcel_info['product_length'] = seq_str1[0]
        parcel_info['product_width'] = seq_str1[2]
        parcel_info['product_height'] = seq_str1[4]
        if seq_str1[5].find(word2) != -1:
            parcel_info['product_dimensions_unit'] = seq_str1[5].strip(word2)
            parcel_info['product_weight'] = seq_str1[6]
            parcel_info['product_weight_unit'] = seq_str1[7]
        else:
            parcel_info['product_dimensions_unit'] = seq_str1[5]
            parcel_info['product_weight'] = None
            parcel_info['product_weight_unit'] = None
        return parcel_info
