# Generated by Django 3.0.2 on 2020-02-24 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0020_auto_20200219_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='dinnerreview',
            name='user_sex',
            field=models.IntegerField(choices=[(0, '不明'), (1, '男性'), (2, '女性')], null=True, verbose_name='性別'),
        ),
    ]
