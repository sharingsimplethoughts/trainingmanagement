# Generated by Django 2.2.2 on 2019-07-15 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0002_auto_20190711_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='menteecourseregistration',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
    ]