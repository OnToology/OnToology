#
# Copyright 2012-2013 Ontology Engineering Group, Universidad Politecnica de Madrid, Spain
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @author Ahmad Alobaid
#


from django.conf.urls import patterns, include, url
from django.contrib import admin
from OnToology import views
from OnToology import dark_views as dark
from django.conf import settings
import api_urls

urlpatterns = patterns('',
    # url(r'^dark_delete_repo', dark.delete_repo, name="dark_deleterepo"),
    # url(r'^dark_update_conf', dark.update_conf, name='dark_updateconf'),
    # # no need to have this in the dark theme as it is not visible for the user and only used to capture webhook payload
    # # url(r'^dark/add_hook', views.add_hook, name='addhook'),
    # # Because it is not straight forward to change the redirect url as it has to be either flipped
    # # e.g. get_access_token/dark
    # url(r'^dark_get_access_token', views.get_access_token, name='getaccesstoken'),
    # # this is not used
    # # url(r'^dark/grantupdate', views.grant_update, name='grantupdate'),
    # url(r'^dark_profile', dark.profile, name='dark_profile'),
    # url(r'^dark_login_get_access', dark.login_get_access, name='dark_login_get_access'),
    # url(r'^dark_login', dark.login, name='dark_login'),
    # url(r'^dark_logout', dark.logout, name='dark_logout'),
    # url(r'^dark_previsual_toggle', dark.previsual_toggle, name='dark_previsualtoggle'),
    # url(r'^dark_renew_previsual', dark.renew_previsual, name='dark_renewprevisual'),
    # url(r'^dark_stepbystep', dark.stepbystep, name='dark_stepbystep'),
    # url(r'^dark_generateforall', dark.generateforall_view, name='dark_generateforall'),
    # url(r'^dark_get_bundle', dark.get_bundle, name='dark_get_bundle'),
    # url(r'^dark_about', dark.about, name='dark_about'),
    # url(r'^dark_home', dark.home, name='dark_home'),

    url(r'^delete_repo', views.delete_repo, name="deleterepo"),
    url(r'^update_conf', views.update_conf, name='updateconf'),
    url(r'^add_hook', views.add_hook, name='addhook'),
    url(r'^get_access_token', views.get_access_token, name='getaccesstoken'),
    url(r'^grantupdate', views.grant_update, name='grantupdate'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^login_get_access', views.login_get_access, name='login_get_access'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^previsual_toggle', views.previsual_toggle, name='previsualtoggle'),
    url(r'^renew_previsual', views.renew_previsual, name='renewprevisual'),
    url(r'^stepbystep', views.stepbystep, name='stepbystep'),
    url(r'^generateforall', views.generateforall_view, name='generateforall'),
    url(r'^get_bundle', views.get_bundle, name='get_bundle'),
    url(r'^about', views.about, name='about'),
    url(r'^api/', include(api_urls)),
    url(r'^progress', views.progress_page),
    url(r'500', views.handler500),
    url(r'faqs', views.faqs),
    # url(r'^admin', views.superadmin, name='superadmin'),
    url(r'', views.home, name='home'),
)

handler500 = 'OnToology.views.handler500'

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns = patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT})) + urlpatterns
