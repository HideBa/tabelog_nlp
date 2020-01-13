# Generated by Django 3.0.2 on 2020-01-11 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='StoreID')),
                ('store_name', models.CharField(max_length=30, verbose_name='StoreName')),
            ],
            options={
                'verbose_name': 'store data',
                'verbose_name_plural': 'store data',
            },
        ),
        migrations.CreateModel(
            name='LunchReview',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='reviewID')),
                ('score', models.FloatField(null=True, verbose_name='each score')),
                ('content', models.TextField(null=True, verbose_name='review content')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sushi_app.Store', verbose_name='store')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'review_lunch',
            },
        ),
    ]
