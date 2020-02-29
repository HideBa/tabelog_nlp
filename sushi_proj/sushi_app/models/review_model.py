from django.db import models
from .store_model import Store
from django.core.validators import MinValueValidator, MaxValueValidator

USER_SEX_LIST = ((0, '不明'), (1, '男性'), (2, '女性'))


class Review(models.Model):
    class Meta:
        verbose_name = 'review'
        verbose_name = 'review'
    id = models.IntegerField('review_dinnerID', primary_key=True)
    ld_id = models.IntegerField('昼OR夜', default=0)
    score = models.FloatField('user score', null=True, validators=[
        MinValueValidator(0),
        MaxValueValidator(5.0)])
    review = models.TextField('review content', null=True)
    is_new = models.BooleanField('新しく取得されたレビューかどうか？', null=True, default=True)
    store = models.ForeignKey(
        Store,
        verbose_name='store',
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return '昼' if self.ld_id == 0 else '夜' + 'レビュー　' + self.content[:30]
