from django.db import models
from .store_model import Store
from django.core.validators import MinValueValidator, MaxValueValidator


class Retty(models.Model):
    class Meta:
        verbose_name = 'retty'
        verbose_name = 'retty'
    id = models.CharField('rrettyID', max_length=10, primary_key=True)
    score = models.FloatField('retty_score')
    store = models.ForeignKey(
        Store,
        verbose_name='store',
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:30]
