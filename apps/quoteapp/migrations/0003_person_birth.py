# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0002_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='birth',
            field=models.DateTimeField(null=True),
        ),
    ]