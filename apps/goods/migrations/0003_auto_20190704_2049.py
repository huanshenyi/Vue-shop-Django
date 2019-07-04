# Generated by Django 2.0 on 2019-07-04 11:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20190703_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotSearchWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(default='', max_length=20, verbose_name='人気キーワード')),
                ('index', models.IntegerField(default=0, verbose_name='並び順')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='挿入時間')),
            ],
            options={
                'verbose_name': '人気キーワード',
                'verbose_name_plural': '人気キーワード',
            },
        ),
        migrations.CreateModel(
            name='IndexAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='goods.GoodsCategory', verbose_name='商品カテゴリー')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='goods.Goods')),
            ],
            options={
                'verbose_name': 'ホームページ商品カテゴリー広告',
                'verbose_name_plural': 'ホームページ商品カテゴリー広告',
            },
        ),
        migrations.RemoveField(
            model_name='goodsimage',
            name='image_url',
        ),
        migrations.AlterField(
            model_name='goodscategorybrand',
            name='image',
            field=models.ImageField(max_length=200, upload_to='brand/'),
        ),
        migrations.AlterModelTable(
            name='goodscategorybrand',
            table='goods_goodsbrand',
        ),
    ]
