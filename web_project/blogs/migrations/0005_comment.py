# Generated by Django 2.1.1 on 2018-10-03 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180914_1255'),
        ('blogs', '0004_auto_20181001_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commented_on', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=100)),
                ('commented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.User')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blogs.Post')),
            ],
        ),
    ]
