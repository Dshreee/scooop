from django.conf.urls import url
from . import views 
urlpatterns = [
    url(r'^panel/manager/list/$',views.manager_list,name='manager_list'),
    url(r'^panel/manager/delete/(?P<pk>\d+)/$',views.manager_delete,name='manager_delete'),
    url(r'^panel/manager/group/$',views.manager_group,name='manager_group'),
    url(r'^panel/manager/group/add/$',views.manager_group_add,name='manager_group_add'),
    url(r'^panel/manager/group/delete/(?P<name>.*)/$',views.manager_group_delete,name='manager_group_delete'),
    url(r'^panel/manager/group/show/(?P<pk>\d+)/$',views.user_groups,name='user_groups'),
    url(r'^panel/manager/group/adduser/(?P<pk>\d+)/$',views.add_user_to_group,name='add_user_to_group'),
    url(r'^panel/manager/group/deluser/(?P<pk>\d+)/(?P<name>.*)/$',views.del_user_from_group,name='del_user_from_group'),
    url(r'^panel/manager/perm/$',views.manager_perm,name='manager_perm'),
    url(r'^panel/manager/perm/delete/(?P<name>.*)/$',views.manager_perm_del,name='manager_perm_del'),
    url(r'^panel/manager/perm/add/$',views.manager_perm_add,name='manager_perm_add'),
    url(r'^panel/manager/perm/show/(?P<pk>\d+)/$',views.user_perms,name='user_perms'),
    url(r'^panel/manager/delperm/(?P<pk>\d+)/(?P<name>.*)/$',views.user_perms_del,name='user_perms_del'),
    url(r'^panel/manager/addperm/(?P<pk>\d+)/$',views.user_perms_add,name='user_perms_add'),
    url(r'^panel/manager/group/addperm/(?P<name>.*)/$',views.group_perms,name='group_perms'),
    url(r'^panel/manager/group/delperm/(?P<gname>.*)/(?P<name>.*)/$',views.group_perms_del,name='group_perms_del'),
     url(r'^panel/manager/group/addpermtogroup/(?P<name>.*)/$',views.group_perms_add,name='group_perms_add'),

]
