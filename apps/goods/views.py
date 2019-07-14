from rest_framework import mixins


from .models import Goods
from .serializers import GoodsSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter

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
    filter_backends = (DjangoFilterBackend,)
    filter_class = GoodsFilter

    # 内容のフィルター追加 -->古い方式
    # def get_queryset(self):
    #     # querysetはsqlを作っただけで、実際取得までに行ってない,データの多さに気にすることはない
    #     queryset = Goods.objects.all()
    #     # フロントエンドからのパラメータを条件として,ここのgetはobject.get(key,default)
    #     price_min = self.request.query_params.get("price_min", 0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset


    # def post(self, request, format=None):
    #     serializer = GoodsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    # from rest_framework import status
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


