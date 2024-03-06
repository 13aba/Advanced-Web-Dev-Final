# Generated by Django 4.2 on 2024-03-06 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0011_alter_feedback_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_by_teachers', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]