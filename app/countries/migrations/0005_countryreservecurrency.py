# Generated by Django 4.1.1 on 2022-12-22 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0004_countrysuiciderate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('CNY', 'CNY'), ('JPY', 'JPY'), ('GBP', 'GBP'), ('AUD', 'AUD'), ('CAD', 'CAD'), ('CHF', 'CHF')], max_length=3, unique=True)),
                ('percentage_in_world_reserves', models.FloatField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CountryReserveCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserve_currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='countries.reservecurrency')),
                ('country', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='reserve_currency', to='countries.country')),
            ],
        ),
    ]
