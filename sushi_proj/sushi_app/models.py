from django.db import models
# from django.contrib.auth.models import User


class Store(models.Model):
    class Meta:
        verbose_name = 'store data'
        verbose_name_plural = 'store data'

    id = models.CharField('StoreID', max_length=6, primary_key=True)
    store_name = models.CharField('StoreName', max_length=30)

    def _str__(self):
        return self.store_name


class ReviewLunch(models.Model):
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
    core_words = models.CharField('軸単語', max_length=20, null=True)
    core_words_count = models.IntegerField('軸単語登場回数', max_length=20, null=True)
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
    
    id = models.CharField('lunch_sentimentanalytics_result', max_length=30, primary_key=True)
    sentense = models.CharField('sentense', max_length=100, null=True)
    sentiment = models.FloatField('sentiment', null=True)
    