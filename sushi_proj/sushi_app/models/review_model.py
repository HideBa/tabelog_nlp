from django.db import models
from .store_model import Store


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


class DinnerReview(models.Model):
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
