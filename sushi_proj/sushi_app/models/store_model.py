from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Store(models.Model):
    class Meta:
        verbose_name = 'store data'
        verbose_name_plural = 'store data'

    id = models.CharField('StoreID', max_length=6, primary_key=True)
    store_name = models.CharField('StoreName', max_length=30)
    tabelog_score = models.FloatField(
        'Tabelog_score', null=True, validators=[
            MinValueValidator(0), MaxValueValidator(5.0)])
    retty_score = models.PositiveIntegerField('Retty_score', null=True)

    def _str__(self):
        return self.store_name
