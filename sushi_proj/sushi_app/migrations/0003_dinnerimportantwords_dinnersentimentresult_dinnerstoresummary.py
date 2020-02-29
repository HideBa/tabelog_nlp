# Generated by Django 3.0.2 on 2020-01-18 03:40

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0002_lunchstoresummary_keyword1_modifier1'),
    ]

    operations = [
        migrations.CreateModel(
            name='DinnerStoreSummary',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='dinner_store_summary')),
                ('keyword1', models.CharField(max_length=20, null=True, verbose_name='keyword1')),
                ('keyword2', models.CharField(max_length=20, null=True, verbose_name='keyword2')),
                ('keyword3', models.CharField(max_length=20, null=True, verbose_name='keyword3')),
                ('keyword4', models.CharField(max_length=20, null=True, verbose_name='keyword4')),
                ('keyword5', models.CharField(max_length=20, null=True, verbose_name='keyword5')),
                ('keyword6', models.CharField(max_length=20, null=True, verbose_name='keyword6')),
                ('keyword7', models.CharField(max_length=20, null=True, verbose_name='keyword7')),
                ('keyword8', models.CharField(max_length=20, null=True, verbose_name='keyword8')),
                ('keyword9', models.CharField(max_length=20, null=True, verbose_name='keyword9')),
                ('keyword10', models.CharField(max_length=20, null=True, verbose_name='keyword10')),
                ('keyword1_modifier1', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20, verbose_name='keyword_modifier1'), null=True, size=None)),
            ],
            options={
                'verbose_name': 'dinner_store_summary',
                'verbose_name_plural': 'dinner_store_summary',
            },
        ),
        migrations.CreateModel(
            name='DinnerSentimentResult',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='lunch_sentimentanalytics_result')),
                ('sentense', models.CharField(max_length=100, null=True, verbose_name='sentense')),
                ('sentiment', models.FloatField(null=True, verbose_name='sentiment')),
                ('magnitude', models.FloatField(null=True, verbose_name='magunitude')),
                ('review', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sushi_app.Review', verbose_name='dinner_review')),
            ],
            options={
                'verbose_name': 'sentiment analytics results',
                'verbose_name_plural': 'sentiment analytics results',
            },
        ),
        migrations.CreateModel(
            name='DinnerImportantWords',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='inportantwordID')),
                ('key_words1', models.CharField(max_length=20, null=True, verbose_name='軸単語1')),
                ('key_words1_count', models.IntegerField(null=True, verbose_name='軸単語1登場回数')),
                ('modifier_word1', models.CharField(max_length=20, null=True, verbose_name='修飾語1')),
                ('modifier_word2', models.CharField(max_length=20, null=True, verbose_name='修飾語2')),
                ('modifier_word3', models.CharField(max_length=20, null=True, verbose_name='修飾語3')),
                ('modifier_word4', models.CharField(max_length=20, null=True, verbose_name='修飾語4')),
                ('modifier_word5', models.CharField(max_length=20, null=True, verbose_name='修飾語5')),
                ('modifier_word6', models.CharField(max_length=20, null=True, verbose_name='修飾語6')),
                ('modifier_word7', models.CharField(max_length=20, null=True, verbose_name='修飾語7')),
                ('modifier_word8', models.CharField(max_length=20, null=True, verbose_name='修飾語8')),
                ('modifier_word9', models.CharField(max_length=20, null=True, verbose_name='修飾語9')),
                ('modifier_word10', models.CharField(max_length=20, null=True, verbose_name='修飾語10')),
                ('store', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sushi_app.Store', verbose_name='store')),
            ],
            options={
                'verbose_name': 'important words',
                'verbose_name_plural': 'important words',
            },
        ),
    ]
