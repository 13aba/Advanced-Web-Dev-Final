# Generated by Django 4.2 on 2024-03-10 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0017_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
