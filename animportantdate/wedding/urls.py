from . import views

from django.conf.urls import url, include

urlpatterns = [
    url(r'^guest/([A-Za-z0-9]{6})/?', views.guest_login),
    url(r'^guest$', views.guest_details),
    url(r'^details/?$', views.content_page, {"page_name": "detail"}),
    url(r'^photos', views.content_page, {"page_name": "photo"}),
    url(r'^gifts', views.content_page, {"page_name": "gift"}),
    url(r'^story', views.content_page, {"page_name": "story"}),
    url(r'^colophon', views.content_page, {"page_name": "colophon"}),
    url(r'^staff/mailout/([0-9]*)', views.mailout),
    url(r'^$', views.index),
]
