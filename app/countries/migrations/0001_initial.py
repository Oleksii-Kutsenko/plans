# Generated by Django 4.1.1 on 2022-12-30 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('iso_code', models.CharField(choices=[('ABW', 'ABW'), ('AFG', 'AFG'), ('AGO', 'AGO'), ('AIA', 'AIA'), ('ALA', 'ALA'), ('ALB', 'ALB'), ('AND', 'AND'), ('ARE', 'ARE'), ('ARG', 'ARG'), ('ARM', 'ARM'), ('ASM', 'ASM'), ('ATA', 'ATA'), ('ATF', 'ATF'), ('ATG', 'ATG'), ('AUS', 'AUS'), ('AUT', 'AUT'), ('AZE', 'AZE'), ('BDI', 'BDI'), ('BEL', 'BEL'), ('BEN', 'BEN'), ('BES', 'BES'), ('BFA', 'BFA'), ('BGD', 'BGD'), ('BGR', 'BGR'), ('BHR', 'BHR'), ('BHS', 'BHS'), ('BIH', 'BIH'), ('BLM', 'BLM'), ('BLR', 'BLR'), ('BLZ', 'BLZ'), ('BMU', 'BMU'), ('BOL', 'BOL'), ('BRA', 'BRA'), ('BRB', 'BRB'), ('BRN', 'BRN'), ('BTN', 'BTN'), ('BVT', 'BVT'), ('BWA', 'BWA'), ('CAF', 'CAF'), ('CAN', 'CAN'), ('CCK', 'CCK'), ('CHE', 'CHE'), ('CHL', 'CHL'), ('CHN', 'CHN'), ('CIV', 'CIV'), ('CMR', 'CMR'), ('COD', 'COD'), ('COG', 'COG'), ('COK', 'COK'), ('COL', 'COL'), ('COM', 'COM'), ('CPV', 'CPV'), ('CRI', 'CRI'), ('CUB', 'CUB'), ('CUW', 'CUW'), ('CXR', 'CXR'), ('CYM', 'CYM'), ('CYP', 'CYP'), ('CZE', 'CZE'), ('DEU', 'DEU'), ('DJI', 'DJI'), ('DMA', 'DMA'), ('DNK', 'DNK'), ('DOM', 'DOM'), ('DZA', 'DZA'), ('ECU', 'ECU'), ('EGY', 'EGY'), ('ERI', 'ERI'), ('ESH', 'ESH'), ('ESP', 'ESP'), ('EST', 'EST'), ('ETH', 'ETH'), ('FIN', 'FIN'), ('FJI', 'FJI'), ('FLK', 'FLK'), ('FRA', 'FRA'), ('FRO', 'FRO'), ('FSM', 'FSM'), ('GAB', 'GAB'), ('GBR', 'GBR'), ('GEO', 'GEO'), ('GGY', 'GGY'), ('GHA', 'GHA'), ('GIB', 'GIB'), ('GIN', 'GIN'), ('GLP', 'GLP'), ('GMB', 'GMB'), ('GNB', 'GNB'), ('GNQ', 'GNQ'), ('GRC', 'GRC'), ('GRD', 'GRD'), ('GRL', 'GRL'), ('GTM', 'GTM'), ('GUF', 'GUF'), ('GUM', 'GUM'), ('GUY', 'GUY'), ('HKG', 'HKG'), ('HMD', 'HMD'), ('HND', 'HND'), ('HRV', 'HRV'), ('HTI', 'HTI'), ('HUN', 'HUN'), ('IDN', 'IDN'), ('IMN', 'IMN'), ('IND', 'IND'), ('IOT', 'IOT'), ('IRL', 'IRL'), ('IRN', 'IRN'), ('IRQ', 'IRQ'), ('ISL', 'ISL'), ('ISR', 'ISR'), ('ITA', 'ITA'), ('JAM', 'JAM'), ('JEY', 'JEY'), ('JOR', 'JOR'), ('JPN', 'JPN'), ('KAZ', 'KAZ'), ('KEN', 'KEN'), ('KGZ', 'KGZ'), ('KHM', 'KHM'), ('KIR', 'KIR'), ('KNA', 'KNA'), ('KOR', 'KOR'), ('KWT', 'KWT'), ('LAO', 'LAO'), ('LBN', 'LBN'), ('LBR', 'LBR'), ('LBY', 'LBY'), ('LCA', 'LCA'), ('LIE', 'LIE'), ('LKA', 'LKA'), ('LSO', 'LSO'), ('LTU', 'LTU'), ('LUX', 'LUX'), ('LVA', 'LVA'), ('MAC', 'MAC'), ('MAF', 'MAF'), ('MAR', 'MAR'), ('MCO', 'MCO'), ('MDA', 'MDA'), ('MDG', 'MDG'), ('MDV', 'MDV'), ('MEX', 'MEX'), ('MHL', 'MHL'), ('MKD', 'MKD'), ('MLI', 'MLI'), ('MLT', 'MLT'), ('MMR', 'MMR'), ('MNE', 'MNE'), ('MNG', 'MNG'), ('MNP', 'MNP'), ('MOZ', 'MOZ'), ('MRT', 'MRT'), ('MSR', 'MSR'), ('MTQ', 'MTQ'), ('MUS', 'MUS'), ('MWI', 'MWI'), ('MYS', 'MYS'), ('MYT', 'MYT'), ('NAM', 'NAM'), ('NCL', 'NCL'), ('NER', 'NER'), ('NFK', 'NFK'), ('NGA', 'NGA'), ('NIC', 'NIC'), ('NIU', 'NIU'), ('NLD', 'NLD'), ('NOR', 'NOR'), ('NPL', 'NPL'), ('NRU', 'NRU'), ('NZL', 'NZL'), ('OMN', 'OMN'), ('PAK', 'PAK'), ('PAN', 'PAN'), ('PCN', 'PCN'), ('PER', 'PER'), ('PHL', 'PHL'), ('PLW', 'PLW'), ('PNG', 'PNG'), ('POL', 'POL'), ('PRI', 'PRI'), ('PRK', 'PRK'), ('PRT', 'PRT'), ('PRY', 'PRY'), ('PSE', 'PSE'), ('PYF', 'PYF'), ('QAT', 'QAT'), ('REU', 'REU'), ('ROU', 'ROU'), ('RUS', 'RUS'), ('RWA', 'RWA'), ('SAU', 'SAU'), ('SDN', 'SDN'), ('SEN', 'SEN'), ('SGP', 'SGP'), ('SGS', 'SGS'), ('SHN', 'SHN'), ('SJM', 'SJM'), ('SLB', 'SLB'), ('SLE', 'SLE'), ('SLV', 'SLV'), ('SMR', 'SMR'), ('SOM', 'SOM'), ('SPM', 'SPM'), ('SRB', 'SRB'), ('SSD', 'SSD'), ('STP', 'STP'), ('SUR', 'SUR'), ('SVK', 'SVK'), ('SVN', 'SVN'), ('SWE', 'SWE'), ('SWZ', 'SWZ'), ('SXM', 'SXM'), ('SYC', 'SYC'), ('SYR', 'SYR'), ('TCA', 'TCA'), ('TCD', 'TCD'), ('TGO', 'TGO'), ('THA', 'THA'), ('TJK', 'TJK'), ('TKL', 'TKL'), ('TKM', 'TKM'), ('TLS', 'TLS'), ('TON', 'TON'), ('TTO', 'TTO'), ('TUN', 'TUN'), ('TUR', 'TUR'), ('TUV', 'TUV'), ('TWN', 'TWN'), ('TZA', 'TZA'), ('UGA', 'UGA'), ('UKR', 'UKR'), ('UMI', 'UMI'), ('URY', 'URY'), ('USA', 'USA'), ('UZB', 'UZB'), ('VAT', 'VAT'), ('VCT', 'VCT'), ('VEN', 'VEN'), ('VGB', 'VGB'), ('VIR', 'VIR'), ('VNM', 'VNM'), ('VUT', 'VUT'), ('WLF', 'WLF'), ('WSM', 'WSM'), ('YEM', 'YEM'), ('ZAF', 'ZAF'), ('ZMB', 'ZMB'), ('ZWE', 'ZWE')], max_length=4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CountryPayingTaxesIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('year', models.IntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s', to='countries.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CountryEconomicFreedomIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('year', models.IntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s', to='countries.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='countrypayingtaxesindex',
            constraint=models.UniqueConstraint(fields=('country', 'year'), name='countries_countrypayingtaxesindex_unique_country_year'),
        ),
        migrations.AddConstraint(
            model_name='countryeconomicfreedomindex',
            constraint=models.UniqueConstraint(fields=('country', 'year'), name='countries_countryeconomicfreedomindex_unique_country_year'),
        ),
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
        migrations.CreateModel(
            name='CountrySuicideRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('year', models.IntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='countries.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='countrysuiciderate',
            constraint=models.UniqueConstraint(fields=('country', 'year'), name='countries_countrysuiciderate_unique_country_year'),
        ),
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
        migrations.CreateModel(
            name='CountryGDP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('year', models.IntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='countries.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='countrygdp',
            constraint=models.UniqueConstraint(fields=('country', 'year'), name='countries_countrygdp_unique_country_year'),
        ),
        migrations.RenameField(
            model_name='countryeconomicfreedomindex',
            old_name='score',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='countrygdp',
            old_name='score',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='countrypayingtaxesindex',
            old_name='score',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='countrysuiciderate',
            old_name='score',
            new_name='value',
        ),
        migrations.CreateModel(
            name='CountryGlobalFinancialCenterIndex',
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
            model_name='countryglobalfinancialcenterindex',
            constraint=models.UniqueConstraint(fields=('country', 'year'), name='countries_countryglobalfinancialcenterindex_unique_country_year'),
        ),
        migrations.CreateModel(
            name='CountryExportsValue',
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
            model_name='countryexportsvalue',
            constraint=models.UniqueConstraint(fields=('country', 'year'), name='countries_countryexportsvalue_unique_country_year'),
        ),
    ]
