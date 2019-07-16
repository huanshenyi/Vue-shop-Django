"""VueShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
import xadmin
from VueShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls

from rest_framework.routers import DefaultRouter
# from goods.views_base import GoodsListView
from goods.views import GoodsListViewSet, CategoryViewSet

router = DefaultRouter()
# goodsのurl設定
router.register(r'goods', GoodsListViewSet, base_name="goods")
# Categoryのurl設定
router.register('categorys', CategoryViewSet, base_name="categorys")


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # drfのドキュメント
    url(r'docs/', include_docs_urls(title="ドキュメント")),

    path('', include(router.urls)),
]
