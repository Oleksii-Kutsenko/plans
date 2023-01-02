# Generated by Django 4.1.1 on 2023-01-01 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0006_countrynatureindex_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryPisaScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('year', models.IntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='countries.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='countrypisascore',
            constraint=models.UniqueConstraint(fields=('country', 'year'), name='countries_countrypisascore_unique_country_year'),
        ),
    ]