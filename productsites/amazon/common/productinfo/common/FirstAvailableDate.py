# extract product date first available
# process the following strings element:
# 'Date First Available : Sep 13, 2021'
# 'Date First Available : Sep 13. 2021'
# 'Date First Available : Sep 13 2021'
# 'Date First Available Sep 13, 2021'
# 'Date First Available : Sept 13, 2021'
# 'Date First Available : Sept 13. 2021'
# 'Date First Available : Sept 13 2021'
# 'Date First Available April 20 2021'
# for uk website date are as follow:
# 'Date First Available 6 April 2021'
# 'Date First Available 9 Jun 2021'


class FirstAvailableDate:
    @staticmethod
    def get_first_date_available(product_details):
        first_date_available = None
        keywords_tbl = 'Date First Available'
        table_block_str = None

        for elem in product_details:
            if keywords_tbl in elem:
                table_block_str = elem

        if table_block_str:
            start_pos = table_block_str.find(keywords_tbl)

            if start_pos != -1:
                start_pos = start_pos + len(keywords_tbl) + 1
                first_date_available = table_block_str[start_pos:]

                if ":" in first_date_available:
                    first_date_available = first_date_available.replace(":", "")
                first_date_available = first_date_available.strip()

                if first_date_available:
                    first_date_available = FirstAvailableDate.format_date(first_date_available)
        return first_date_available

    # format the following date: Sept. 29 2020 to Sep. 29 2020
    @staticmethod
    def format_date(date):
        str_date = date
        if "," in date:
            str_date = date.replace(",", "")
        if "." in str_date:
            str_date = str_date.replace(".", "")
        str_date_list = str_date.split()
        if str_date[0].isnumeric():
            month_formatted = str_date_list[1][:3]
            date_formatted = month_formatted + " " + str_date_list[0] + " " + str_date_list[2]
        else:
            month_formatted = str_date_list[0][:3]
            date_formatted = month_formatted + " " + str_date_list[1] + " " + str_date_list[2]
        return date_formatted
