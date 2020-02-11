from django.contrib import admin
# from sushi_app.models import Store, LunchReview, LunchImportantWords, DinnerReview, LunchSentimentResult, StoreSummary
from sushi_app.models.store_model import Store
from sushi_app.models.review_model import LunchReview, DinnerReview
from sushi_app.models.important_word_model import LunchImportantWords, DinnerImportantWords
from sushi_app.models.sentiment_result_model import LunchSentimentResult, DinnerSentimentResult
from sushi_app.models.store_summary import LunchStoreSummary, DinnerStoreSummary

admin.site.register(Store)
admin.site.register(LunchReview)
admin.site.register(LunchImportantWords)
admin.site.register(DinnerImportantWords)
admin.site.register(LunchSentimentResult)
admin.site.register(DinnerSentimentResult)
admin.site.register(LunchStoreSummary)
admin.site.register(DinnerStoreSummary)
admin.site.register(DinnerReview)