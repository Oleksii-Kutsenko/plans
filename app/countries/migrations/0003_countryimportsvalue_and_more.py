# Generated by Django 4.1.1 on 2022-12-31 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0002_auto_20221230_0636'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryImportsValue',
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
            model_name='countryimportsvalue',
            constraint=models.UniqueConstraint(fields=('country', 'year'), name='countries_countryimportsvalue_unique_country_year'),
        ),
    ]
