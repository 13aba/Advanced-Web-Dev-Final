# Generated by Django 4.2 on 2024-03-06 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_post_file_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(editable=False)),
                ('score', models.IntegerField()),
                ('content', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.appuser')),
            ],
        ),
    ]
