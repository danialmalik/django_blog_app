# Generated by Django 2.1.1 on 2018-10-10 07:07

import base.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20181010_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, null=True, validators=[base.utils.not_in_future]),
        ),
    ]
