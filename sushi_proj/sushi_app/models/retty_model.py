from django.db import models


class Retty(models.Model):
    class Meta:
        verbose_name = 'retty'
        verbose_name = 'retty'
    id = models.IntegerField('rettyID', primary_key=True)
    score = models.FloatField('retty_score')
    phone_num = models.CharField('電話番号', max_length=20)
    name = models.CharField('name', max_length=30, null=True)

    def __str__(self):
        return 'retty ' + str(self.score)
