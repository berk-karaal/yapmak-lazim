# Generated by Django 3.2.6 on 2021-12-13 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('update_date', models.DateTimeField(auto_now_add=True)),
                ('is_marked', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('color', models.CharField(choices=[('white', 'white'), ('tomato', 'tomato'), ('aqua', 'aqua'), ('skyblue', 'skyblue'), ('coral', 'coral')], default='white', max_length=20)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
