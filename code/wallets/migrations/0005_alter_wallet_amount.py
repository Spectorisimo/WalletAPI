# Generated by Django 4.1.7 on 2023-04-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0004_remove_wallet_is_blocked_wallet_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
        ),
    ]
