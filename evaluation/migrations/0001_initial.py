# Generated by Django 3.2.7 on 2022-05-05 11:00

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
            name='EssayQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=256, null=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RatingQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=256, null=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q_1', models.PositiveIntegerField(blank=True, null=True)),
                ('q_2', models.PositiveIntegerField(blank=True, null=True)),
                ('q_3', models.PositiveIntegerField(blank=True, null=True)),
                ('q_4', models.PositiveIntegerField(blank=True, null=True)),
                ('q_5', models.PositiveIntegerField(blank=True, null=True)),
                ('q_6', models.PositiveIntegerField(blank=True, null=True)),
                ('q_7', models.PositiveIntegerField(blank=True, null=True)),
                ('q_8', models.PositiveIntegerField(blank=True, null=True)),
                ('e_1', models.TextField(blank=True, null=True)),
                ('e_2', models.TextField(blank=True, null=True)),
                ('e_3', models.TextField(blank=True, null=True)),
                ('e_4', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]