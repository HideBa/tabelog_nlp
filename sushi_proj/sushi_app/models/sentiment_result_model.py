from django.db import models
from .review_model import LunchReview


class LunchSentimentResult(models.Model):
    class Meta:
        verbose_name = 'sentiment analytics results'
        verbose_name_plural = 'sentiment analytics results'

    id = models.CharField(
        'lunch_sentimentanalytics_result',
        max_length=30,
        primary_key=True)
    sentense = models.CharField('sentense', max_length=100, null=True)
    sentiment = models.FloatField('sentiment', null=True)
    magnitude = models.FloatField('magunitude', null=True)
    review = models.OneToOneField(
        LunchReview,
        verbose_name='lunch_review',
        on_delete=models.CASCADE)
