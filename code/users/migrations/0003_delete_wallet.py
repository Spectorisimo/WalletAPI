# Generated by Django 4.1.7 on 2023-03-31 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wallet',
        ),
    ]