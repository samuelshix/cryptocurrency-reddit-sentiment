# Generated by Django 4.0.1 on 2022-06-19 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.TextField(max_length=20, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('subreddit', models.TextField(default='cryptocurrency', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=3)),
            ],
        ),
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
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.TextField(max_length=20, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=10000)),
                ('score', models.IntegerField()),
                ('date', models.DateField()),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.submission')),
                ('topic', models.ManyToManyField(related_name='topics', to='app.Topic')),
            ],
        ),
    ]
