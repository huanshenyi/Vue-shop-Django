from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from .serializers import SmsSerializer, UserRegSerializer
from rest_framework.response import Response
from rest_framework import status
User = get_user_model()
from .models import VerifyCode
from random import choice

# 電話番号の認証、今使わない
# from utils.yunpian import YunPian

class CustomBackend(ModelBackend):
    """
    userの認証をカスタマイズ
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    検証コードを送信
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        四桁code
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # スマートフォン新規ユーザーの想定code
        # mobile = serializer.validated_data["mobile"]
        # yun_pian = YunPian(APIKEY)
        # code = self.generate_code
        # ms_status = yun_pian.send_sms(code=code,mobile=mobile)
        # if sms_status['code'] == 0:
        #   return Response({"mobile":sms_status["msg"]},status=status.HTTP_400_BAD_REQUEST)
        # else:
        #   code_record = VerifyCode(code=code, mobile=mobile)
        #   code_record.save()
        #   return Response({"mobile":mobile}, status=status.HTTP_201_CREATED)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    user
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()