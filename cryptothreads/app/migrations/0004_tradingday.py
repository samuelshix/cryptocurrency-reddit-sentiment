# Generated by Django 4.0.1 on 2022-06-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_comment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradingDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('crypto_cap', models.IntegerField()),
                ('ethereum_price', models.IntegerField()),
                ('bitcoin_price', models.IntegerField()),
            ],
        ),
    ]
