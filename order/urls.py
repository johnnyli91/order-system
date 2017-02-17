from django.conf.urls import url
from views import add_to_cart, calculate_total, get_web_order_menu, \
    view_cart, remove_from_cart, get_menu

urlpatterns = [
    url(r'^add_to_cart/$', add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart/$', remove_from_cart, name='remove_from_cart'),
    url(r'^calculate/$', calculate_total, name='calculate_total'),
    url(r'^web_order_menu/$', get_web_order_menu, name='get_web_order_menu'),
    url(r'^cart/$', view_cart, name='view_cart'),
    url(r'^menu/$', get_menu, name='menu')
]
