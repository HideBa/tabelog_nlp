# Generated by Django 3.0.2 on 2020-02-09 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0014_auto_20200209_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dinnersentimentresult',
            name='sentense',
            field=models.CharField(max_length=1000, null=True, verbose_name='sentense'),
        ),
        migrations.AlterField(
            model_name='lunchsentimentresult',
            name='sentense',
            field=models.CharField(max_length=1000, null=True, verbose_name='sentense'),
        ),
    ]
