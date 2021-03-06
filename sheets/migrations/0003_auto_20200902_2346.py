# Generated by Django 3.1 on 2020-09-02 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0002_auto_20200902_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.CharField(max_length=30, null=True, verbose_name='이메일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='kind',
            field=models.CharField(blank=True, choices=[('준비위', '준비위'), ('발표자', '발표자')], default='발표자', max_length=15, null=True),
        ),
    ]
