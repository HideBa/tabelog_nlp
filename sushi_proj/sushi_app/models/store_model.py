from django.db import models


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
