# Generated by Django 2.1.1 on 2018-09-14 12:55

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, null=True, validators=[users.models.not_in_future]),
        ),
    ]
