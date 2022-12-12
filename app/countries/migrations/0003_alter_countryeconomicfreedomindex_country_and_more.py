# Generated by Django 4.1.1 on 2022-12-11 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0002_countrypayingtaxesindex_countryeconomicfreedomindex_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countryeconomicfreedomindex',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='countries.country'),
        ),
        migrations.AlterField(
            model_name='countrypayingtaxesindex',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='countries.country'),
        ),
    ]
