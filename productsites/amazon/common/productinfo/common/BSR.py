# Extract Best Seller Rank: up to 4 layers : GrandFather Father and Son
# handle the following that starts with '#':
# Type 1: BSR
# #Amazon Best Sellers Rank: #154 in Sports & Outdoors (See Top 100 in Sports & Outdoors) #292inWomen's Shops#16inWomen's Athletic Shorts#36inRunning Clothing
# #292inWomen's Shops
# #16inWomen's Athletic Shorts
# #36inRunning Clothing
# Type 2: BSR
# #Amazon Best Sellers Rank: #154 in Sports & Outdoors (See Top 100 in Sports & Outdoors) #292inWomen's Shops#16inWomen's Athletic Shorts#36inRunning Clothing
# Type 3: BSR
# #Amazon Best Sellers Rank: #154 in Sports & Outdoors (See Top 100 in Sports & Outdoors)
# #292inWomen's Shops
# #16inWomen's Athletic Shorts
# #36inRunning Clothing

class BSR:
    # Amazon Best Sellers Rank: #160 in Sports & Outdoors (See Top 100 in Sports & Outdoors) #306inWomen's Shops#16inWomen's Athletic Shorts#40inRunning Clothing
    @staticmethod
    def get_product_bsr(product_details):
        product_bsr = None
        keywords_tbl = 'Best Sellers Rank'
        table_block_str = None
        dash_char = '#'
        flag_exists = False

        # reassemble Best seller rank elements in one string which is: (table_block_str)
        for elem in product_details:
            if keywords_tbl in elem:
                table_block_str = elem
                flag_exists = True
            # get all element that starts with '#'
            if (elem.startswith(dash_char)) and flag_exists:
                table_block_str = table_block_str + elem
        if table_block_str:
            start_pos = table_block_str.find(keywords_tbl)
            if start_pos != -1:
                start_pos = start_pos + len(keywords_tbl) + 1
                product_bsr_str = table_block_str[start_pos:]
                if ":" in product_bsr_str:
                    product_bsr_str = product_bsr_str.replace(":", "")
                product_bsr_str = product_bsr_str.strip()
                if product_bsr_str is not None:
                    product_bsr = BSR.process_seller_rank(product_bsr_str)
        return product_bsr

    # handle string like this (starts with #)
    # #160 in Sports & Outdoors (See Top 100 in Sports & Outdoors) #306inWomen's Shops#16inWomen's Athletic Shorts#40inRunning Clothing
    @staticmethod
    def process_seller_rank(seller_rank_str):
        cat_array = []
        cat_rank_array = []
        seller_rank = {'category': None, 'category_rank': None,
                       'sub_category': None, 'sub_category_rank': None, 'sub_sub_category': None,
                       'sub_sub_category_rank': None, 'category_sub4': None, 'category_sub4_rank': None}
        keywords_tbl = ['#', 'in', '(', ')']
        dash_in_bsr_str = seller_rank_str.find(keywords_tbl[0])
        if dash_in_bsr_str != -1:
            str_list = seller_rank_str.split(keywords_tbl[0])
            i = 0
            while i < len(str_list):
                if i == 1:
                    end_pos = str_list[i].find(keywords_tbl[2])
                    if end_pos != -1:
                        str_cat = str_list[i][:end_pos]
                        flag_index = str_cat.find(keywords_tbl[1])
                        if flag_index != -1:
                            str_cat_list = str_cat.split(keywords_tbl[1], 1)
                            seller_rank['category_rank'] = str_cat_list[0].strip()
                            seller_rank['category'] = str_cat_list[1].strip()
                else:
                    if i != 0:
                        if keywords_tbl[1] in str_list[i]:
                            str_cat_list = str_list[i].split(keywords_tbl[1], 1)
                            cat_str_rank = str_cat_list[0].strip()
                            cat_str = str_cat_list[1].strip()
                            cat_array.append(cat_str)
                            cat_rank_array.append(cat_str_rank)
                i += 1
            cat_array_temp = []
            cat_rank_array_temp = []
            for k in range(0, len(cat_array)):
                if cat_array[k] not in cat_array_temp:
                    cat_array_temp.append(cat_array[k])
                    cat_rank_array_temp.append(cat_rank_array[k])
            for t in range(0, len(cat_array_temp)):
                if t == 0:  # fill level 2 category and its rank
                    seller_rank['sub_category'] = cat_array_temp[t]
                    seller_rank['sub_category_rank'] = cat_rank_array_temp[t]
                else:
                    if t == 1:  # fill level 3 category and its rank
                        seller_rank['sub_sub_category'] = cat_array_temp[t]
                        seller_rank['sub_sub_category_rank'] = cat_rank_array_temp[t]
                    else:
                        if t == 2:  # fill level 4 category and its rank
                            seller_rank['category_sub4'] = cat_array_temp[t]
                            seller_rank['category_sub4_rank'] = cat_rank_array_temp[t]
        return seller_rank
