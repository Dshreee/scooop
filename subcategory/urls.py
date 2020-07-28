from django.conf.urls import url
from . import views 
urlpatterns = [

    url(r'^panel/subcategory/list/$',views.subcategory_list,name='subcategory_list'),
    url(r'^panel/subcategory/add/$',views.subcategory_add,name='subcategory_add'),

   
]
