from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status

from .models import Goods
from .serializers import GoodsSerializer
from rest_framework.pagination import PageNumberPagination

from rest_framework import viewsets

# Create your views here.
# ページング設定
class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    # page_query_param = 'p'


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品リストページ
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination



    # def post(self, request, format=None):
    #     serializer = GoodsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    # from rest_framework import status
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


