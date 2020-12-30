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


from django.conf.urls import include, url
from django.contrib import admin
from OnToology import views
from django.conf import settings
from OnToology import api_urls


urlpatterns = [
    url(r'^delete_repo', views.delete_repo, name="deleterepo"),
    url(r'^update_conf', views.update_conf, name='updateconf'),
    url(r'^add_hook', views.add_hook, name='addhook'),
    url(r'^get_access_token', views.get_access_token, name='getaccesstoken'),
    url(r'^grantupdate', views.grant_update, name='grantupdate'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^repos', views.repos_view, name='repos'),
    url(r'^ontologies', views.get_ontologies, name='ontologies'),
    url(r'^runs', views.runs_view, name='runs'),
    # url(r'^repo', views.repo_view, name='repo'),
    url(r'^login_get_access', views.login_get_access, name='login_get_access'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^previsual_toggle', views.previsual_toggle, name='previsualtoggle'),
    url(r'^renew_previsual', views.renew_previsual, name='renewprevisual'),
    url(r'^stepbystep', views.stepbystep, name='stepbystep'),
    url(r'^publications', views.publications, name='publications'),
    url(r'^generateforall', views.generateforall_view, name='generateforall'),
    url(r'^get_bundle', views.get_bundle, name='get_bundle'),
    url(r'^about', views.about, name='about'),
    url(r'^api/', include(api_urls)),
    url(r'^progress', views.progress_page),
    url(r'500', views.handler500),
    url(r'faqs', views.faqs),
    url(r'get_branches', views.get_branches),
    url(r'get_outline', views.get_outline),
    url(r'^show_repos_list', views.show_repos_list),
    url(r'^get_repos_list_file', views.get_repos_list_file),
    url(r'^publish', views.publish_view),
    url(r'^update_stats', views.update_stats_view),
    url(r'^syntax', views.syntax_check_view),
    url(r'show_stats', views.show_stats),
    # url(r'^error_test', views.error_test),
    # url(r'^admin', views.superadmin, name='superadmin'),
    url(r'', views.home, name='home'),
]

handler500 = 'OnToology.views.handler500'

# if settings.DEBUG:
#     # static files (images, css, javascript, etc.)
#     urlpatterns = ['',
#         (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#             'document_root': settings.MEDIA_ROOT})] + urlpatterns


if settings.DEBUG:
    from django.conf.urls.static import static
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
