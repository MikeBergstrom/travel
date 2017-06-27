from django.conf.urls import url
from . import views

app_name = "trips"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^create$', views.create, name="create"),
    url(r'^join/(?P<id>\d+)$', views.join, name="join"),
    url(r'^show/(?P<id>\d+)$', views.show, name="show")
]

