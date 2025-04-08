# Generated by Django 5.1.6 on 2025-04-07 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_blog_tenant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tenantusers',
            options={'verbose_name': 'Tenant User', 'verbose_name_plural': 'Tenant Users'},
        ),
        migrations.AddField(
            model_name='blog',
            name='JsonContent',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='htmlContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='tenantusers',
            unique_together={('tenant', 'user')},
        ),
    ]
