# Generated by Django 2.0.2 on 2019-02-04 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0005_auto_20190123_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='eng_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='英語名'),
        ),
    ]
