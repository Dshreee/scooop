from django.conf.urls import url
from . import views 
urlpatterns = [
    #if u want to write 127.0.0.1:8000/home
    url(r'home/$',views.home , name='home'),
    #if u want to write 127.0.0.1:8000
    #url(r'^/$',views.home , name='home')
   url(r'^about/$',views.about , name='about'),
   url(r'^panel/$',views.panel,name='panel'),
   url(r'^login/$',views.mylogin,name='mylogin'),
   url(r'^logout/$',views.mylogout,name='mylogout'),
   url(r'^change/password/$',views.changepass,name='changepass'),
   url(r'^register/$',views.myregister,name='myregister'),
   url(r'^settings/$',views.site_settings,name='site_settings'),

]
















