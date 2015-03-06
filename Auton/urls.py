from django.conf.urls import patterns, include, url
from django.contrib import admin
from Auton import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Auton.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^home',views.home),
    #url(r'^admin/', include(admin.site.urls)),
)
