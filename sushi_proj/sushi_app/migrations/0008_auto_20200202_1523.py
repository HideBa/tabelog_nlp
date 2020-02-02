# Generated by Django 3.0.2 on 2020-02-02 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0007_auto_20200202_1442'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dinnerimportantwords',
            options={'verbose_name': 'dinner important words', 'verbose_name_plural': 'dinner important words'},
        ),
        migrations.AlterModelOptions(
            name='lunchimportantwords',
            options={'verbose_name': 'lunch important words', 'verbose_name_plural': 'lunch important words'},
        ),
        migrations.AlterField(
            model_name='dinnersentimentresult',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sushi_app.DinnerReview', verbose_name='dinner_review'),
        ),
    ]
