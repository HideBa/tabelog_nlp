from django.db import models
from .store_model import Store


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
        '軸単語1登場回数', null=True)
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


class DinnerImportantWords(models.Model):
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
        '軸単語1登場回数', null=True)
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
