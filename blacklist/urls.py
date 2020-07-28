from django.conf.urls import url
from . import views 
urlpatterns = [
    url(r'^panel/manager/blacklist/$',views.blacklist,name='blacklist'),
    url(r'^panel/manager/blacklist/add/$',views.blacklist_add,name='blacklist_add'),
    url(r'^panel/manager/blacklist/del/(?P<ip>.*)/$',views.blacklist_delete,name='blacklist_delete'),
]
