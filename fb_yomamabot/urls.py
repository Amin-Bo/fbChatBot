# yomamabot/fb_yomamabot/urls.py
from django.conf.urls import include, url
from .views import YoMamaBotView
urlpatterns = [
    url(r'^81b3488408b1e47b727a24e187ecb5c612b981a4da17bd51b8/?$',
        YoMamaBotView.as_view())
]
