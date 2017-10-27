# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 23:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quoteby', models.CharField(max_length=55)),
                ('quotation', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('favorited', models.ManyToManyField(related_name='favorited_quotes', to='quoteapp.Person')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_quotes', to='quoteapp.Person')),
            ],
        ),
    ]