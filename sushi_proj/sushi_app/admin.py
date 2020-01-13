from django.contrib import admin
from .models import Store, LunchReview, LunchImportantWords, DinnerReview, LunchSentimentResult, StoreSummary
# Register your models here.


admin.site.register(Store)
admin.site.register(LunchReview)
admin.site.register(LunchImportantWords)
admin.site.register(LunchSentimentResult)
admin.site.register(StoreSummary)
