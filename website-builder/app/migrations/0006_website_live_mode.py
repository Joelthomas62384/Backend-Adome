# Generated by Django 5.1.6 on 2025-04-02 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_website_web_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='live_mode',
            field=models.BooleanField(default=False),
        ),
    ]
