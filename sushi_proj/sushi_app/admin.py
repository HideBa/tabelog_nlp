from django.contrib import admin
# from sushi_app.models import Store, LunchImportantWords, Review, LunchSentimentResult, StoreSummary
from sushi_app.models.store_model import Store
from sushi_app.models.review_model import Review
from sushi_app.models.important_word_model import LunchImportantWords, DinnerImportantWords
from sushi_app.models.sentiment_result_model import LunchSentimentResult, DinnerSentimentResult
from sushi_app.models.store_summary import LunchStoreSummary, DinnerStoreSummary
from sushi_app.models.dinner_summary_average import DinnerSummaryAverage
from sushi_app.models.score_history_model import TabelogHistory, RettyHistory


admin.site.register(Store)
admin.site.register(LunchImportantWords)
admin.site.register(DinnerImportantWords)
admin.site.register(LunchSentimentResult)
admin.site.register(DinnerSentimentResult)
admin.site.register(LunchStoreSummary)
admin.site.register(DinnerStoreSummary)
admin.site.register(Review)
admin.site.register(DinnerSummaryAverage)
admin.site.register(TabelogHistory)
admin.site.register(RettyHistory)
