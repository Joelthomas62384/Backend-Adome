# Generated by Django 5.1.6 on 2025-02-22 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tenants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('subscription_plan', models.CharField(choices=[('1', 'Free'), ('2', 'Premium')], default='1', max_length=100)),
                ('logo', models.TextField(blank=True, null=True)),
                ('domain', models.CharField(max_length=250, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('founding_year', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('blog', models.BooleanField(default=True)),
                ('community', models.BooleanField(default=False)),
                ('newsletter', models.BooleanField(default=False)),
                ('subdomain', models.CharField(max_length=150, unique=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usercache')),
            ],
        ),
    ]
