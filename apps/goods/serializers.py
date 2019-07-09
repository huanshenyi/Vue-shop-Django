from rest_framework import serializers

from goods.models import Goods, GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(required=True, max_length=100)
    # click_num = serializers.IntegerField(default=0)
    # goods_front_image = serializers.ImageField()

    # def create(self, validated_data):
    #     return Goods.objects.create(**validated_data)
    category = CategorySerializer()
    class Meta:
        model = Goods
        fields = "__all__"
        # fields = ('name', 'click_num', 'market_price', 'add_time')