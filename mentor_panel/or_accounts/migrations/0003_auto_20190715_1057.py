# Generated by Django 2.2.2 on 2019-07-15 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('or_accounts', '0002_auto_20190715_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='mentee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cert_mentee', to='accounts.RegisteredUser'),
        ),
    ]
