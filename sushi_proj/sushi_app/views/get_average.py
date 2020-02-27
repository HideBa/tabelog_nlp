from sushi_proj.settings import BASE_DIR
from django.core.exceptions import ObjectDoesNotExist
from sushi_app.models.store_model import Store
from sushi_app.models.review_model import LunchReview, DinnerReview
from sushi_app.models.sentiment_result_model import LunchSentimentResult, DinnerSentimentResult
from sushi_app.models.important_word_model import LunchImportantWords, DinnerImportantWords
from sushi_app.models.store_summary import DinnerStoreSummary, LunchStoreSummary
from sushi_app.models.dinner_summary_average import DinnerSummaryAverage


def get_keyword_average(keyword):
    average_obj = DinnerSummaryAverage.objects.get(keyword__exact=keyword)
    return average_obj.keyword_sentiment_ave_score
