# Generated by Django 5.1.6 on 2025-05-23 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_communitychats_optimistic_uui'),
    ]

    operations = [
        migrations.RenameField(
            model_name='communitychats',
            old_name='optimistic_uui',
            new_name='optimistic_uuid',
        ),
    ]
