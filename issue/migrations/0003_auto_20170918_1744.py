# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0002_auto_20170918_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuerecord',
            name='issue_time',
            field=models.DateTimeField(null=True),
        ),
    ]
