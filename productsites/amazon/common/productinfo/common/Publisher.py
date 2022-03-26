# extract Publisher:
# may not be needed since we already get the manufacturer and also the brand.

class Publisher:

    # needs a method here to get publisher
    # also need to add publisher to items.py

    # process the following Publisher to get date and publisher name exp:
    # BodyBoss (Jan. 1 2017)
    @staticmethod
    def get_seller_brand_and_date(brand_date):
        keywords_tbl = ['(', ')']
        brand_date_table = [None, None]

        start_pos = brand_date.find(keywords_tbl[0])
        end_pos = start_pos + 1
        split_brand_date_str = brand_date.split(brand_date[start_pos:end_pos])
        brand_date_table[0] = split_brand_date_str[0].strip()
        brand_date_table[1] = split_brand_date_str[1].strip(')')
        return brand_date_table
