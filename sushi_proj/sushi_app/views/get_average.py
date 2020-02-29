
from sushi_app.models.dinner_summary_average import DinnerSummaryAverage


def get_keyword_average(keyword):
    average_obj = DinnerSummaryAverage.objects.get(keyword__exact=keyword)
    return average_obj.keyword_sentiment_ave_score
