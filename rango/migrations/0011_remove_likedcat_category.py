# Generated by Django 2.1.5 on 2021-08-04 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0010_auto_20210804_1024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likedcat',
            name='category',
        ),
    ]
