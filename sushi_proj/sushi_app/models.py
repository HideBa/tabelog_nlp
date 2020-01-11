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
        verbose_name = 'review'
        verbose_name_plural = 'review_lunch'
    # temporary set 'null' for development. in product set it null=False
    id = models.CharField('reviewID', max_length=10, primary_key=True)
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
