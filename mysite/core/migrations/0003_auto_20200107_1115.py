# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-01-07 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200107_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulations',
            name='netlist_content',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='simulations',
            name='simulation_output_text',
            field=models.TextField(null=True),
        ),
    ]
