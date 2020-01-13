from django.db import models
from django.contrib.postgres.fields import ArrayField


class LunchStoreSummary(models.Model):
    class Meta:
        verbose_name = 'lunch_store_summary'
        verbose_name_plural = 'lunch_store_summary'
    id = models.CharField(
        'lunch_store_summary',
        max_length=6,
        primary_key=True)
    keyword1 = models.CharField('keyword1', max_length=20, null=True)
    keyword2 = models.CharField('keyword2', max_length=20, null=True)
    keyword3 = models.CharField('keyword3', max_length=20, null=True)
    keyword4 = models.CharField('keyword4', max_length=20, null=True)
    keyword5 = models.CharField('keyword5', max_length=20, null=True)
    keyword6 = models.CharField('keyword6', max_length=20, null=True)
    keyword7 = models.CharField('keyword7', max_length=20, null=True)
    keyword8 = models.CharField('keyword8', max_length=20, null=True)
    keyword9 = models.CharField('keyword9', max_length=20, null=True)
    keyword10 = models.CharField('keyword10', max_length=20, null=True)

# -------------positive negative --------------------
    keyword1_modifier1 = ArrayField(
        models.CharField(
            'keyword_modifier1',
            max_length=20),
        null=True)
    # ex.) ['強い', '120', '30']
