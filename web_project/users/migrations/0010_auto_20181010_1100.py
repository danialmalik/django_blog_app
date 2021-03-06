# Generated by Django 2.1.1 on 2018-10-10 06:00

import base.utils
from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20181010_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(null=True, validators=[base.utils.not_in_future]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/empty.png', upload_to=users.models._get_upload_path),
        ),
    ]
