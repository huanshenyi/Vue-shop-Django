# Generated by Django 2.0 on 2019-08-19 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0003_auto_20190704_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfav',
            name='user',
            field=models.ForeignKey(help_text='ユーザーid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
    ]
