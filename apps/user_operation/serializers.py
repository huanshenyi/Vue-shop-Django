from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ("goods", "id")


# 商品をお気に入りにする際にログインしてるユーザーを選ぶ
# https://www.django-rest-framework.org/api-guide/validators/#advanced-field-defaults
class UserFavSeriallzer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        help_text='ログインしてるユーザー'
    )
    class Meta:
        model = UserFav
        # お気に入りデータの単一性,modelでも設定可能,最低二つのカラムが必要なため、単独に設定できない
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="既にお気に入り済みです"
            )
        ]

        fields = ("user", "goods", "id")