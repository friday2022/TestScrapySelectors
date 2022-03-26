# extract Number of product Answered Questions
import logging

logger = logging.getLogger()


class Questions:

    @staticmethod
    def get_nb_answered_questions(item):
        try:
            answered_questions_count = item['answered_questions_count']

            if answered_questions_count:
                answered_questions_count = answered_questions_count.strip()
                nbaq_list = answered_questions_count.split()
                return nbaq_list[0]
        except KeyError as ke:
            pass

        return ''
