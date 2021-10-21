# Generated by Django 3.2.8 on 2021-10-21 11:53

from django.db import migrations, models
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
                ('content', models.TextField()),
                ('logo', pyuploadcare.dj.models.ImageField()),
                ('attachments', pyuploadcare.dj.models.ImageGroupField(blank=True, null=True)),
            ],
        ),
    ]
