from django.db import models
from .store_model import Store
from django.core.validators import MinValueValidator, MaxValueValidator


class TabelogHistory(models.Model):
    class Meta:
        verbose_name = 'tabelog_history'
        verbose_name = 'tabelog_history'
    id = models.CharField(
        'tabelog_history_ID',
        max_length=20,
        primary_key=True)
    score = models.FloatField('user score', null=True, validators=[
        MinValueValidator(0),
        MaxValueValidator(5.0)])
    nth = models.PositiveIntegerField('何回目')
    created_at = models.DateTimeField('データ作成日時', auto_now=True, null=True)
    store = models.ForeignKey(
        Store,
        verbose_name='store',
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.score) + " " + str(self.nth)


class RettyHistory(models.Model):
    class Meta:
        verbose_name = 'retty_history'
        verbose_name = 'retty_history'
    id = models.CharField('retty_history_ID', max_length=20, primary_key=True)
    score = models.FloatField('user score', null=True, validators=[
        MinValueValidator(0)])
    nth = models.PositiveIntegerField('何回目')
    created_at = models.DateTimeField('データ作成日時', auto_now=True, null=True)
    store = models.ForeignKey(
        Store,
        verbose_name='store',
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.score) + " " + str(self.nth)
