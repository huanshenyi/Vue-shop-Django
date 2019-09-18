__author__ = "txy1226052@gmail.com"
import time
from rest_framework import serializers
from goods.models import Goods
from .models import ShoppingCart, OrderInfo
from goods.serializers import GoodsSerializer


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields = "__all__"


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
        goods_num = validated_data["goods_num"] # フロントエンド多分num使ってる
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

    def update(self, instance, validated_data):
        # 商品の数を修正
        instance.goods_num = validated_data["goods_num"]
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    def generate_order_sn(self):
        # オーダー番号:現在時間+user_id+ランダム数
        from random import Random
        time_str = time.strftime("%Y%m%d%H%M%S")
        user_id = self.context["request"].user.id
        random_ins = Random().randint(10, 99)
        order_sn = f"{time_str}{user_id}{random_ins}"
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
      model = OrderInfo
      fields = "__all__"

