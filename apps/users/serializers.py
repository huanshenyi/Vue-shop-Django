import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import VerifyCode

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
