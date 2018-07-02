# Generated by Django 2.0.6 on 2018-07-02 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foodsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='APImodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apikey', models.CharField(default=None, max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('usage', models.IntegerField(default=0)),
                ('limit', models.IntegerField(default=0)),
                ('resettime', models.TimeField(default=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]