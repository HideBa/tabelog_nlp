from django.db import models
from django.contrib.postgres.fields import ArrayField
from .store_model import Store


class DinnerSummaryAverage(models.Model):
    class Meta:
        verbose_name = 'dinner_summary_average'
        verbose_name_plural = 'dinner_summary_average'
    id = models.CharField(
        'dinner_summary_average',
        max_length=10,
        primary_key=True)
    keyword = models.CharField('keyword', max_length=30, null=True)
    keyword_sentiment_ave_score = models.FloatField(
        'sentiment_ave_score', null=True)
