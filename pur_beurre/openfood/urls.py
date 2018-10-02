from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^recherche/$', views.search_product, name='search_product'),
    url(r'^un-produit-au-hasard/$', views.ramdom_product, name='ramdom_product'),
    url(r'^(?P<pk>\d+)/substituts/$', views.product_substitutes, name='product_substitutes'),
]



