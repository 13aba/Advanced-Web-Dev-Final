# Generated by Django 4.2 on 2024-02-26 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='isStudent',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
    ]
