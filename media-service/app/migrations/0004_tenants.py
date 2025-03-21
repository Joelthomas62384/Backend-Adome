# Generated by Django 5.1.6 on 2025-02-26 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_logo_logoimages_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('subdomain', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Tenant',
                'verbose_name_plural': 'Tenants',
            },
        ),
    ]
