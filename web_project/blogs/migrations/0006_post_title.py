# Generated by Django 2.1.1 on 2018-10-03 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='title', max_length=25),
            preserve_default=False,
        ),
    ]
