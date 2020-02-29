from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Store(models.Model):
    class Meta:
        verbose_name = 'store data'
        verbose_name_plural = 'store data'

    id = models.CharField('StoreID', max_length=6, primary_key=True)
    # id = models.IntegerField('StoreID', primary_key=True)
    store_name = models.CharField('StoreName', max_length=30)
    tabelog_score = models.FloatField(
        'Tabelog_score', null=True, validators=[
            MinValueValidator(0), MaxValueValidator(5.0)])
    station = models.CharField('最寄り駅', max_length=20, null=True)
    lunch_price = models.CharField('ランチ価格', max_length=10, null=True)
    dinner_price = models.CharField('ディナー価格', max_length=10, null=True)
    address = models.CharField('住所', max_length=50, null=True)
    phone_num = models.CharField('電話番号', max_length=11, default='000')
    opening_time = models.CharField('営業時間', max_length=20, null=True)
    regular_holiday = models.CharField('定休日', max_length=10, null=True)
    url = models.URLField('url', null=True)
    latitude = models.FloatField('latitude', null=True)
    longitude = models.FloatField('longtitude', null=True)
    retty_score = models.PositiveIntegerField('Retty_score', null=True)
    created_at = models.DateTimeField('データ作成日時', auto_now=True, null=True)
    updated_at = models.DateTimeField('データ作成日時', auto_now_add=True, null=True)
    tabelog_growth_rate = models.FloatField('食べログ伸び率', null=True)
    retty_growth_rate = models.FloatField('Retty伸び率', null=True)

    def _str__(self):
        return self.store_name
