# Generated by Django 3.1 on 2020-09-17 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0007_auto_20200918_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.TextField(default='', null=True, verbose_name='발표제목'),
        ),
    ]
