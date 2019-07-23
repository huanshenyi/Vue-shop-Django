# url=https://django-filter.readthedocs.io/en/master/guide/rest_framework.html#quickstart
import django_filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品フィルタークラス
    """
    pricemin = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    topcategory = django_filters.NumberFilter(method="top_category_filter")
    # 曖昧捜査
    # name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # topカテゴリー下のすべての商品
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) |
                                   Q(category__parent_category__parent_category_id=value))


    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']