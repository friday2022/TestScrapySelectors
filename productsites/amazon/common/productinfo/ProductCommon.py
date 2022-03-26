# Extract : Product Information
# The following fields will be extracted:
# customer_reviews : number of reviews
# Parcel Dimensions or Product Dimensions with:
# product_length
# product_width
# product_height
# product_dimensions_unit
# product_weight
# product_weight_unit
# product_ASIN  OR product_ISBN (If ASIN is not available)
# product_brand
# date_first_available
# best_sellers_rank

# from . import imageslinks as imglinks
# from . import urllinktoreviews as rl

import re
from .common import BSR as bsr
from .common import Category as cat
from .common import Manufacturer as mnf
from .common import Reviews as Rcs
from .common import SentimentScore as ss
from .common import CategoryScore as cs
from .common import Dimensions as dim
from .common import ProductNumber as pn
from .common import ISBN as isbn
from .common import Brand as br
from .common import FirstAvailableDate as fad
from .common import Questions as qst

from bs4 import BeautifulSoup


class ProductCommon:

    @staticmethod
    def product_common_info(product, common):
        product['title'] = common['title']
        product['answered_questions_count'] = qst.Questions.get_nb_answered_questions(common)
        all_table_html_removed = ProductCommon.get_and_clean_html(common)
        product['product_ASIN'] = pn.ProductNumber.get_product_number(all_table_html_removed)
        product['date_first_available'] = fad.FirstAvailableDate.get_first_date_available(all_table_html_removed)
        product['product_brand'] = br.Brand.get_product_brand(all_table_html_removed, common)
        product['best_sellers_rank'] = bsr.BSR.get_product_bsr(all_table_html_removed)
        if product['best_sellers_rank']:
            product['product_category'] = cat.Category.get_product_category(product['best_sellers_rank'])
            product['sellingFactor'] = cs.CategoryScore.get_category_score(product['best_sellers_rank'])
        else:
            product['product_category'] = None
            product['sellingFactor'] = None
        product['parcel_dimensions'] = dim.Dimensions.get_product_dimensions(all_table_html_removed)
        product['manufacturer'] = mnf.Manufacturer.get_manufacturer_name(all_table_html_removed)
        product['product_ISBN'] = isbn.ISBN.get_product_isbn(all_table_html_removed)
        product['customer_reviews'] = Rcs.Reviews.get_reviews_count_score(all_table_html_removed,
                                                                          common)
        if product['customer_reviews']:
            product['reviewSentimentScore'] = ss.SentimentScore.get_sentiment_score(product['customer_reviews'])
        else:
            product['reviewSentimentScore'] = None


    @staticmethod
    def get_and_clean_html(common):
        if common['product_information_template1']:
            str_with_html = common['product_information_template1']
        else:
            if common['product_information_template2']:
                str_with_html = common['product_information_template2']
            else:
                str_with_html = None
        if str_with_html:
            product_details_formatted = ProductCommon.clean_product_details(str_with_html)
        else:
            product_details_formatted = None
        return product_details_formatted

    @staticmethod
    def clean_product_details(str_block):
        # remove known unwanted patterns
        str_block = str_block.replace("    ", "")
        html = str_block.replace("&gt;&gt;&gt;", "")
        # regularize multiple spaces
        html = re.sub(r"\s{2,}", " ", html)
        # construct soup (DOM)
        soup = BeautifulSoup(html, 'html.parser')
        # extract text in target elements (2 templates for table found in scrapper)
        el = soup.find_all("li")
        if not el:
            el = soup.find_all("tr")
        el_text = [((p.get_text()).encode('ascii', 'ignore')).decode("utf-8") for p in el]
        # remove '\n' for each element in the list
        new_els = []
        for each_e in el_text:
            new_el = each_e.replace("\n", "").strip()
            new_els.append(new_el)
        # remove element having 'Manufacturer reference' (otherwise it will cause pb with 'Manufacturer')
        str1 = 'Manufacturer reference'
        for e in new_els:
            if str1 in e:
                new_els.remove(e)

        return new_els
