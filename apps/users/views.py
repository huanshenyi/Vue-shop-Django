from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
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


class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    user
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    # tokenも返す
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_payload_handler(payload)
        re_dict['name'] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        serializer.save()