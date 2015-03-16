from django.conf.urls import patterns, include, url
from django.contrib import admin
from Auton import views

from django.conf import settings



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Auton.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^add_hook',views.add_hook,name='addhook'),
    url(r'attach_webhook',views.attach_webhook,name="attachwebhook"),
    url(r'^get_access_token',views.get_access_token,name='getaccesstoken'),
    url(r'^deleterepo',views.delete_repo,name='deleterepo'),
    url(r'^grantupdate',views.grant_update,name='grantupdate'),
    url(r'',views.home, name='home'),
    #url(r'^admin/', include(admin.site.urls)),
)




if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns = patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})) + urlpatterns
