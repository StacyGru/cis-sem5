# Generated by Django 3.2.9 on 2021-11-13 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'city',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=64)),
                ('first_middle_name', models.CharField(db_column='first&middle_name', max_length=128)),
                ('gender', models.CharField(max_length=1)),
                ('date_of_birth', models.DateField()),
                ('place_of_birth', models.CharField(max_length=256)),
                ('status', models.CharField(blank=True, max_length=17, null=True)),
            ],
            options={
                'db_table': 'client',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(db_column='date&time')),
                ('organization', models.CharField(max_length=9)),
                ('sum', models.IntegerField()),
            ],
            options={
                'db_table': 'contract',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=64)),
                ('rate', models.FloatField()),
            ],
            options={
                'db_table': 'currency_rate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=64)),
                ('first_middle_name', models.CharField(db_column='first&middle_name', max_length=128)),
                ('gender', models.CharField(max_length=1)),
                ('position', models.CharField(max_length=13)),
                ('organization', models.CharField(max_length=9)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('photo', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'employee',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=64)),
                ('hotel_name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256)),
                ('number_of_stars', models.CharField(max_length=11)),
            ],
            options={
                'db_table': 'hotel',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HotelReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_room', models.IntegerField()),
                ('room_type', models.CharField(max_length=11)),
                ('check_in_date', models.DateField(db_column='check-in_date')),
                ('check_out_date', models.DateField()),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'hotel_reservation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('series', models.IntegerField(primary_key=True, serialize=False)),
                ('number', models.IntegerField()),
                ('passport_type', models.CharField(max_length=11)),
                ('date_of_issue', models.DateField()),
                ('expiration_date', models.DateField()),
                ('issued_by', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'passport',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(db_column='date&time')),
                ('organization', models.CharField(max_length=9)),
                ('sum_in_rubles', models.IntegerField()),
            ],
            options={
                'db_table': 'payment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PreliminaryAgreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(db_column='date&time')),
                ('organization', models.CharField(max_length=9)),
                ('number_of_trip_participants', models.IntegerField()),
                ('country_of_visit', models.CharField(max_length=64)),
                ('trip_start_date', models.DateField()),
                ('trip_end_date', models.DateField()),
            ],
            options={
                'db_table': 'preliminary_agreement',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Synchronization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(db_column='date&time')),
                ('organization', models.CharField(max_length=9)),
                ('file', models.TextField()),
            ],
            options={
                'db_table': 'synchronization',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_place', models.CharField(max_length=128)),
                ('arrival_place', models.CharField(max_length=128)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('transport_type', models.CharField(max_length=7)),
                ('transfer', models.IntegerField()),
                ('travel_document_number', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'trip',
                'managed': False,
            },
        ),
    ]
