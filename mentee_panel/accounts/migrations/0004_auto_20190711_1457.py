# Generated by Django 2.2.2 on 2019-07-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_registereduser_is_profile_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='registereduser',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='mobile',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
