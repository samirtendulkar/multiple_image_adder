# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-04-05 01:22
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=250, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=500, unique=True)),
                ('message', models.TextField()),
                ('message_html', models.TextField(editable=False)),
                ('post_image', models.ImageField(upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Prep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='images/')),
                ('image_title', models.CharField(default='', max_length=100)),
                ('image_description', models.CharField(default='', max_length=250)),
                ('sequence', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_prep', to='posts.Post')),
            ],
            options={
                'ordering': ['sequence'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='prep',
            unique_together=set([('post', 'sequence')]),
        ),
    ]