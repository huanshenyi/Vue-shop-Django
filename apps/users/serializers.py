import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import VerifyCode
from rest_framework.validators import UniqueValidator

from VueShop.settings import REGEX_MOBILE

User = get_user_model()


# メール認証用の
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=20)

    def validate_mobile(self, mobile):
        """
        携帯番号の認証
        :param data:
        :return:
        """
        # 既にあるのかどうか
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("ユーザー存在する")

        # 番号の形式合ってか
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("モバイルナンバー形式エラー")

        # 頻度の制限
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("送信は一分以上空いてください")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    user詳細表示用
    """
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")


class UserRegSerializer(serializers.ModelSerializer):
     # code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,
     #                              error_messages={"required": "codeを入力してください",
     #                                              "blank":"codeを入力してください",
     #                                              "max_length": "形式合ってない"},help_text="検証コート")
     username = serializers.CharField(required=True, allow_blank=False, label="ユーザーネーム",
                                      validators=[UniqueValidator(queryset=User.objects.all(), message="ユーザー存在する")])
                                                                                    # write_only=True に設定すれば、戻されない
     password = serializers.CharField(style={'input_type': 'password'}, label="パスワード", write_only=True)

     # 保存前のdetaを取得
     # def create(self, validated_data):
     #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
     #     user.set_password(validated_data['password'])
     #     user.save()
     #     return user

     # def validate_code(self, code):
     #     # try:
     #     #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"])
     #     # except VerifyCode.DoesNotExist as e:
     #     #       pass
     #     # except VerifyCode.MultipleObjectsReturned as e:
     #     #     pass
     #
     #     # self.initial_data == フロントからの値  | get使用しない理由は二つの結果あるかもしれません、codeはランダムのため
     #     verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
     #     if verify_records:
     #         last_records = verify_records[0]
     #         five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
     #         if five_mintes_ago > last_records.add_time:
     #             raise serializers.ValidationError('code時間切れ')
     #
     #         if last_records.code != code:
     #             raise serializers.ValidationError('code合ってない')
     #     else:
     #         raise serializers.ValidationError('code存在しない')

     # 全てdataのバリデーション
     # def validate(self, attrs):
     #     attrs["mobile"] = attrs["username"]
     #     del attrs["code"]
     #     return attrs

     class Meta:
         model = User
         fields = ("username", "mobile", "password", "email")