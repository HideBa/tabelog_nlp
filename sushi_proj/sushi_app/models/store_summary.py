from django.db import models
from django.contrib.postgres.fields import ArrayField
from .store_model import Store


class LunchStoreSummary(models.Model):
    class Meta:
        verbose_name = 'lunch_store_summary'
        verbose_name_plural = 'lunch_store_summary'
    id = models.CharField(
        'lunch_store_summary',
        max_length=30,
        primary_key=True)
    store = models.ForeignKey(
        Store,
        verbose_name='store',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    keyword1 = models.CharField('keyword1', max_length=20, null=True)

# -------------positive negative --------------------
    keyword1_modifier1 = ArrayField(
        models.CharField(
            'keyword_modifier1',
            max_length=20),
        null=True)
    # ex.) ['強い', '120', '30']


class DinnerStoreSummary(models.Model):
    class Meta:
        verbose_name = 'dinner_store_summary'
        verbose_name_plural = 'dinner_store_summary'
    id = models.CharField(
        'dinner_store_summary',
        max_length=30,
        primary_key=True)
    store = models.ForeignKey(
        Store,
        verbose_name='store',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    # on_delete=models.CASCADE, related_name='dinner_summary')
    created_at = models.DateTimeField('データ作成日時', auto_now=True, null=True)
    updated_at = models.DateTimeField('データ作成日時', auto_now_add=True, null=True)

    keyword = models.CharField('keyword1', max_length=20, null=True)
    keyword_sentiment = ArrayField(
        models.CharField(
            'keyword_sentiment',
            max_length=10),
        null=True)

# -------------positive negative --------------------
# keyword1--------------------
    keyword_modifier1 = ArrayField(
        models.CharField(
            'keyword_modifier1',
            max_length=20),
        null=True)
    # ex.) ['強い', '120', '30']
    keyword_modifier2 = ArrayField(
        models.CharField(
            'keyword_modifier1',
            max_length=20),
        null=True)
    keyword_modifier3 = ArrayField(
        models.CharField(
            'keyword_modifier1',
            max_length=20),
        null=True)
    keyword_modifier4 = ArrayField(
        models.CharField(
            'keyword_modifier1',
            max_length=20),
        null=True)
    keyword_modifier5 = ArrayField(
        models.CharField(
            'keyword_modifier1',
            max_length=20),
        null=True)
    keyword_modifier6 = ArrayField(
        models.CharField(
            'keyword_modifier1',
            max_length=20),
        null=True)
    # keyword_modifier7 = ArrayField(
    #     models.CharField(
    #         'keyword_modifier1',
    #         max_length=20),
    #     null=True)
    # keyword_modifier8 = ArrayField(
    #     models.CharField(
    #         'keyword_modifier1',
    #         max_length=20),
    #     null=True)
    # keyword_modifier9 = ArrayField(
    #     models.CharField(
    #         'keyword_modifier1',
    #         max_length=20),
    #     null=True)
    # keyword_modifier10 = ArrayField(
    #     models.CharField(
    #         'keyword_modifier1',
    #         max_length=20),
    #     null=True)
