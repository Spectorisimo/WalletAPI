# Generated by Django 4.1.7 on 2023-04-03 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0002_alter_wallet_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='wallet_number',
            field=models.CharField(blank=True, editable=False, max_length=10, null=True, unique=True),
        ),
    ]