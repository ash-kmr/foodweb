# Generated by Django 2.0.6 on 2018-07-02 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodsite', '0004_auto_20180702_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apimodel',
            name='apikey',
            field=models.CharField(default=None, max_length=15),
        ),
    ]