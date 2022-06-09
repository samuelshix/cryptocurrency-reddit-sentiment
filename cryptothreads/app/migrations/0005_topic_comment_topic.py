# Generated by Django 4.0.1 on 2022-06-07 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_tradingday'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('gen', 'General'), ('btc', 'Bitcoin'), ('eth', 'Ethereum')], default='gen', max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='topic',
            field=models.ManyToManyField(to='app.Topic'),
        ),
    ]
