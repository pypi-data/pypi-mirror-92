# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-11-13 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aimmo', '0021_add_pdf_names_to_worksheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
