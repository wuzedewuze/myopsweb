from django.conf.urls import include, url
from accounts import views, user, group, permission

urlpatterns = [
    url(r'^login/$', views.UserLoginView.as_view(), name='user_login'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name="user_logout"),
    #url(r'^user/list/$', views.UserListView.as_view(), name="user_list"),
    url(r'^user/list/$', user.UserListView.as_view(), name="user_list"),

    url(r'^user/', include([
        url(r'^modify/', include([
            url(r'^status/$', user.ModifyUserStatusView.as_view(), name="user_modify_status"),
            url(r'^group/$', user.ModifyUserGroupView.as_view(), name="user_modify_group"),
        ]))
    ])),

    url(r'^group/', include([
        url(r'^$', group.GroupListView.as_view(), name="group_list"),
        url(r'^create/$', group.GroupCreateView.as_view(), name="group_create"),
        url(r'^userlist/$',group.GroupUserList.as_view(), name="group_userlist"),
        url(r'^permission/', include([
            url(r'^modify/$', group.ModifyGroupPermissionList.as_view(), name="group_permission_modify"),
            url(r'^show/$',group.ShowGroupPermissionList.as_view(),name="group_permission_show"),
            url(r'^delete/$',group.GroupDeleteView.as_view(),name="group_permission_delete")
        ])),
    ])),

    url(r'^permission/', include([
        url(r'^list/$', permission.PermissionListView.as_view(), name="permission_list"),
        url(r'^add/$', permission.PermissionCreateView.as_view(), name="permission_create"),
    ]))
]
