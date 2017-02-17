from django.conf.urls import include, url
from django.contrib import admin
from order.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'order/', include('order.urls')),
    url(r'^$', index)
]
