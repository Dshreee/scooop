from django.conf.urls import url
from . import views 
urlpatterns = [
    url(r'^panel/newsletter/add/$',views.newsletter , name='newsletter'),
    url(r'^panel/newsletter/email/$',views.newsletter_email , name='newsletter_email'),
    url(r'^panel/newsletter/contact/$',views.newsletter_contact , name='newsletter_contact'),
    url(r'^panel/newsletter/del/(?P<pk>\d+)/(?P<status>\d+)/$',views.newsletter_del , name='newsletter_del'),
    url(r'^export/newsletter/csv/$',views.export_newsletter_csv,name='export_newsletter_csv'),
]
