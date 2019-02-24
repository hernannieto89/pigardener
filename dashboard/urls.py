from django.conf.urls import url
from django.urls import path, reverse

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^edit/(?P<pk>\d+)/$', views.EditSimpleTimer.as_view(), name='edit'),
    url(r'^switch_status/(?P<id>\d+)/$', views.switch_status, name='switch_status'),

]
