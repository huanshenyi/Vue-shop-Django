# Generated by Django 2.0 on 2019-07-04 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0002_auto_20190703_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='city',
            field=models.CharField(default='', max_length=100, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='province',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='県'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='district',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='地域'),
        ),
    ]
