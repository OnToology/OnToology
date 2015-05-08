from django.conf.urls import patterns, include, url
from django.contrib import admin
from Auton import views

from django.conf import settings



urlpatterns = patterns('',
    url(r'^add_hook_test',views.add_hook_test,name='addhooktest'),
    url(r'^add_hook',views.add_hook,name='addhook'),
    url(r'^get_access_token',views.get_access_token,name='getaccesstoken'),
    url(r'^grantupdate',views.grant_update,name='grantupdate'),
    url(r'^testlogin',views.testlogin,name='testlogin'),
    url(r'^login_get_access',views.login_get_access,name='login_get_access'),
    url(r'^login',views.login,name='login'),
    url(r'^logout',views.logout,name='logout'),
    url(r'',views.home, name='home'),
)




if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns = patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})) + urlpatterns
