from django.conf.urls import patterns, include, url
from django.contrib import admin
from OnToology import views

from django.conf import settings



urlpatterns = patterns('',
    url(r'^delete_repo',views.delete_repo,name="deleterepo"),
    url(r'^update_conf',views.update_conf,name='updateconf'),
    url(r'^add_hook',views.add_hook,name='addhook'),
    url(r'^get_access_token',views.get_access_token,name='getaccesstoken'),
    url(r'^grantupdate',views.grant_update,name='grantupdate'),
    url(r'^profile',views.profile,name='profile'),
    url(r'^login_get_access',views.login_get_access,name='login_get_access'),
    url(r'^login',views.login,name='login'),
    url(r'^logout',views.logout,name='logout'),
    url(r'^previsual_toggle',views.previsual_toggle,name='previsualtoggle'),
    url(r'^renew_previsual',views.renew_previsual,name='renewprevisual'),
    url(r'',views.home, name='home'),
)




if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns = patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})) + urlpatterns
