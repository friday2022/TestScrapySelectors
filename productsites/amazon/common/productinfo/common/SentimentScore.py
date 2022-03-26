# extract sentiment score from customer review score - specific to scrapper

class SentimentScore:
    @staticmethod
    def get_sentiment_score(review_score):
        return review_score['reviews_score']