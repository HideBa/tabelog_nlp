from django.db import models
from .review_model import Review
from .store_model import Store
from django.core.validators import MinValueValidator, MaxValueValidator


class LunchSentimentResult(models.Model):
    class Meta:
        verbose_name = 'lunch sentiment analytics results'
        verbose_name_plural = 'lunch sentiment analytics results'

    id = models.CharField(
        'lunch_sentimentanalytics_result',
        max_length=30,
        primary_key=True)
    sentense = models.CharField('sentense', max_length=1000, null=True)
    sentiment = models.FloatField('sentiment', null=True, validators=[
                                  MinValueValidator(-1.0), MaxValueValidator(1.0)])
    magnitude = models.FloatField('magunitude', null=True)
    review = models.OneToOneField(
        Review,
        verbose_name='lunch_review',
        on_delete=models.CASCADE)


class DinnerSentimentResult(models.Model):
    class Meta:
        verbose_name = 'dinner sentiment analytics results'
        verbose_name_plural = 'dinner sentiment analytics results'

    id = models.CharField(
        'lunch_sentimentanalytics_result',
        max_length=30,
        primary_key=True)
    created_at = models.DateTimeField('データ作成日時', auto_now=True, null=True)
    updated_at = models.DateTimeField('データ作成日時', auto_now_add=True, null=True)
    sentense = models.CharField('sentense', max_length=1000, null=True)
    sentiment = models.FloatField('sentiment', null=True, validators=[
                                  MinValueValidator(-1.0), MaxValueValidator(1.0)])
    magnitude = models.FloatField('magunitude', null=True)
    review = models.ForeignKey(
        Review,
        verbose_name='dinner_review',
        on_delete=models.CASCADE)
    store = models.ForeignKey(
        Store,
        null=True,
        verbose_name='store',
        on_delete=models.CASCADE)
