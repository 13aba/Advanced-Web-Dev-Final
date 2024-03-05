# Generated by Django 4.2 on 2024-03-05 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('due_date', models.DateField(editable=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.course')),
            ],
        ),
    ]