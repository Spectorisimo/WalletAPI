# Generated by Django 4.1.7 on 2023-03-31 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_number', models.PositiveIntegerField(blank=True, editable=False, null=True, unique=True)),
                ('name', models.CharField(default='Мой кошелёк', max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('amount_currency', models.CharField(choices=[('KZT', 'Kzt'), ('EUR', 'Eur'), ('USD', 'Usd')], default='KZT', max_length=3)),
                ('is_blocked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wallets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
