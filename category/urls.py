from django.conf.urls import url
from . import views 
urlpatterns = [

    url(r'^panel/category/list/$',views.category_list,name='category_list'),
    url(r'^panel/category/add/$',views.category_add,name='category_add'),
    url(r'^export/category/csv/$',views.export_cat_csv,name='export_cat_csv'),
    url(r'^import/category/csv/$',views.import_cat_csv,name='import_cat_csv'),
   
]
