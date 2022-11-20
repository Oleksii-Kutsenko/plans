# Generated by Django 4.1.1 on 2022-11-20 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0004_rename_lazyportfolioticker_portfolioticker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioticker',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickers', to='investments.portfolio'),
        ),
    ]