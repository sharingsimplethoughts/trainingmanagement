# Generated by Django 2.2.2 on 2019-07-22 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_registereduser_has_dual_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='registereduser',
            name='payment',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
