__author__ = "txy1226052@gmail.com"

from rest_framework import serializers
from goods.models import Goods
from .models import ShoppingCart


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        help_text='ログインしてるユーザー'
    )
    goods_num = serializers.IntegerField(required=True, min_value=1,
                                         error_messages={"min_value": "商品の数は1以下あってはならない",
                                                         "required": "購入数を入れてください"
                                                         })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        goods_num = validated_data["num"] # フロントエンド多分num使ってる
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            # 商品存在する場合数を上乗せする
            existed = existed[0]
            existed.goods_num += goods_num
            existed.save()
        else:
            # 商品存在しなければ追加
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

