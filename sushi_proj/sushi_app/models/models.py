from django.db import models
from django.contrib.postgres.fields import ArrayField
# from django.contrib.auth.models import User


class Store(models.Model):
    class Meta:
        verbose_name = 'store data'
        verbose_name_plural = 'store data'

    id = models.CharField('StoreID', max_length=6, primary_key=True)
    store_name = models.CharField('StoreName', max_length=30)
    tabelog_score = models.FloatField('Tabelog_score', null=True)
    retty_score = models.PositiveIntegerField('Retty_score', null=True)

    def _str__(self):
        return self.store_name


class LunchReview(models.Model):
    class Meta:
        verbose_name = 'review_lunch'
        verbose_name_plural = 'review_lunch'
    # temporary set 'null' for development. in product set it null=False
    id = models.CharField('review_lunchID', max_length=10, primary_key=True)
    score = models.FloatField('each score', null=True)
    content = models.TextField('review content', null=True)
    store = models.ForeignKey(
        Store,
        verbose_name='store',
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:30]


class ReviewDinner(models.Model):
    class Meta:
        verbose_name = 'review_dinner'
        verbose_name = 'review_dinner'
    id = models.CharField('review_dinnerID', max_length=10, primary_key=True)
    score = models.FloatField('user score', null=True)
    content = models.TextField('review content', null=True)
    store = models.ForeignKey(
        Store,
        verbose_name='store',
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:30]


class LunchImportantWords(models.Model):
    class Meta:
        verbose_name = 'important words'
        verbose_name_plural = 'important words'
    id = models.CharField('inportantwordID', max_length=10, primary_key=True)
    store = models.OneToOneField(
        Store,
        verbose_name='store',
        on_delete=models.CASCADE)
    key_words1 = models.CharField('軸単語1', max_length=20, null=True)
    key_words1_count = models.IntegerField(
        '軸単語1登場回数', max_length=20, null=True)
    modifier_word1 = models.CharField('修飾語1', max_length=20, null=True)
    modifier_word2 = models.CharField('修飾語2', max_length=20, null=True)
    modifier_word3 = models.CharField('修飾語3', max_length=20, null=True)
    modifier_word4 = models.CharField('修飾語4', max_length=20, null=True)
    modifier_word5 = models.CharField('修飾語5', max_length=20, null=True)
    modifier_word6 = models.CharField('修飾語6', max_length=20, null=True)
    modifier_word7 = models.CharField('修飾語7', max_length=20, null=True)
    modifier_word8 = models.CharField('修飾語8', max_length=20, null=True)
    modifier_word9 = models.CharField('修飾語9', max_length=20, null=True)
    modifier_word10 = models.CharField('修飾語10', max_length=20, null=True)


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


class LunchStoreSummary(models.Model):
    class Meta:
        verbose_name = 'lunch_store_summary'
        verbose_name_plural = 'lunch_store_summary'
    id = models.CharField(
        'lunch_store_summary',
        max_length=6,
        primary_key=True)
    keyword1 = models.CharField('keyword1', max_length=20, null=True)
    keyword2 = models.CharField('keyword2', max_length=20, null=True)
    keyword3 = models.CharField('keyword3', max_length=20, null=True)
    keyword4 = models.CharField('keyword4', max_length=20, null=True)
    keyword5 = models.CharField('keyword5', max_length=20, null=True)
    keyword6 = models.CharField('keyword6', max_length=20, null=True)
    keyword7 = models.CharField('keyword7', max_length=20, null=True)
    keyword8 = models.CharField('keyword8', max_length=20, null=True)
    keyword9 = models.CharField('keyword9', max_length=20, null=True)
    keyword10 = models.CharField('keyword10', max_length=20, null=True)
    keyword1_modifier1 = ArrayField(
        models.CharField(
            'modifier1', max_length=10, null=True), models.FloatField(
            'sentiment', null=True), models.FloatField(
                'magnitude', null=True), size=3)
    keyword1_modifier1 = ArrayField(
        models.CharField(
            'modifier1', max_length=10, null=True), models.FloatField(
            'sentiment', null=True), models.FloatField(
                'magnitude', null=True), size=3)
    keyword1_modifier1 = ArrayField(
        models.CharField(
            'modifier1', max_length=10, null=True), models.FloatField(
            'sentiment', null=True), models.FloatField(
                'magnitude', null=True), size=3)
    keyword1_modifier1 = ArrayField(
        models.CharField(
            'modifier1', max_length=10, null=True), models.FloatField(
            'sentiment', null=True), models.FloatField(
                'magnitude', null=True), size=3)
    keyword1_modifier1 = ArrayField(
        models.CharField(
            'modifier1', max_length=10, null=True), models.FloatField(
            'sentiment', null=True), models.FloatField(
                'magnitude', null=True), size=3)
    keyword1_modifier1 = ArrayField(
        models.CharField(
            'modifier1', max_length=10, null=True), models.FloatField(
            'sentiment', null=True), models.FloatField(
                'magnitude', null=True), size=3)
