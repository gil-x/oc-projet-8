from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^favoris/', views.user_favorites, name='user_favorites'),
    url(r'^add-product/(?P<pk>\d+)/$', views.add_to_favorites, name='add_to_favorites'),
    url(r'^remove-product/(?P<pk>\d+)/$', views.remove_from_favorites, name='remove_from_favorites'),
]




