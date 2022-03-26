import logging
from datetime import datetime

logger = logging.getLogger()


# This class is not used now (get date arrives directly
class ArrivalDate:
    @staticmethod
    def get_product_arrival_date(buy_now):
        try:
            if buy_now['arrives_date1']:
                return ArrivalDate.format_arrival_date(buy_now['arrives_date1'])
            elif buy_now['arrives_date2']:
                return ArrivalDate.format_arrival_date(buy_now['arrives_date2'])
        except KeyError as ke:
            pass
        logger.error('New Date_arrives selector in Buying Options to be included in selector file')
        return ''

    # convert 'Wednesday, February 9' to 20220209
    # convert 'February 25 - March 18' to 20220225
    @staticmethod
    def format_arrival_date(arrival_date):
        is_comma = ','
        is_hyphen = '-'
        current_year = datetime.today().strftime('%Y')
        if is_comma in arrival_date:
            month_and_day = arrival_date.split(is_comma)[1].strip()
            date_to_format = month_and_day + ' ' + current_year
            return datetime.strptime(date_to_format, '%B %d %Y').strftime('%Y%m%d')
        elif is_hyphen in arrival_date:
            month_and_day = arrival_date.split(is_hyphen)[0].strip()
            date_to_format = month_and_day + ' ' + current_year
            return datetime.strptime(date_to_format, '%B %d %Y').strftime('%Y%m%d')
        else:
            return arrival_date
