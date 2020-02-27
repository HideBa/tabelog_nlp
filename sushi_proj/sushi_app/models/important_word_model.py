from django.db import models
from .store_model import Store
from django.contrib.postgres.fields import ArrayField


class LunchImportantWords(models.Model):
    class Meta:
        verbose_name = 'lunch important words'
        verbose_name_plural = 'lunch important words'
    id = models.CharField('inportantwordID', max_length=10, primary_key=True)
    store = models.OneToOneField(
        Store,
        verbose_name='store',
        on_delete=models.CASCADE)
    all_words_num = models.IntegerField('総単語数', null=True)
    key_words = models.CharField('軸単語', max_length=20, null=True)
    key_words_nums = models.IntegerField('軸単語出現数', null=True)
    key_words_count = models.IntegerField(
        '軸単語登場回数', null=True)
    keyword_modifier1 = ArrayField(
        models.CharField(
            'keyword_modifier1',
            max_length=20),
        null=True)
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

# 以下修正の必要あり


class DinnerImportantWords(models.Model):
    class Meta:
        verbose_name = 'dinner important words'
        verbose_name_plural = 'dinner important words'
    id = models.CharField('inportantwordID', max_length=10, primary_key=True)
    store = models.ForeignKey(
        Store,
        verbose_name='store',
        on_delete=models.CASCADE)
    all_words_num = models.IntegerField('総単語数', null=True)
    key_words = models.CharField('軸単語', max_length=20, null=True)
    key_words_nums = models.IntegerField('軸単語出現数', null=True)
    created_at = models.DateTimeField('データ作成日時', auto_now=True, null=True)
    keyword_modifier1 = ArrayField(
        models.CharField(
            'keyword_modifier1',
            max_length=20),
        null=True)
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
