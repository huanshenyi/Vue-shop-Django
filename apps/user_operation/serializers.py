from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav
from .models import UserLeavingMessage
from .models import UserAddress
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


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        help_text='ログインしてるユーザー'
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
       model = UserLeavingMessage
       fields = ("user", "msg_type", "subject", "message", "file", "id", 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        help_text='ログインしてるユーザー'
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    address = serializers.CharField(required=True, allow_blank=False, label="送り先")
    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", 'add_time', 'signer_mobile')