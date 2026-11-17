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


from django.urls import include, re_path


from OnToology import views
from django.conf import settings
from OnToology import api_urls


urlpatterns = [
    re_path(r'^delete_repo', views.delete_repo_view, name="deleterepo"),
    re_path(r'^update_conf', views.update_conf, name='updateconf'),
    re_path(r'^add_hook', views.add_hook, name='addhook'),
    re_path(r'^get_access_token', views.get_access_token, name='getaccesstoken'),
    re_path(r'^grantupdate', views.grant_update, name='grantupdate'),
    re_path(r'^profile', views.profile, name='profile'),
    re_path(r'^repos', views.repos_view, name='repos'),
    re_path(r'^ontologies', views.get_ontologies, name='ontologies'),
    re_path(r'^runs', views.runs_view, name='runs'),
    re_path(r'^opub', views.opub_view, name='opub'),
    re_path(r'^login_get_access', views.login_get_access, name='login_get_access'),
    re_path(r'^login', views.login, name='login'),
    re_path(r'^logout', views.logout, name='logout'),
    re_path(r'^previsual_toggle', views.previsual_toggle, name='previsualtoggle'),
    re_path(r'^renew_previsual', views.renew_previsual, name='renewprevisual'),
    re_path(r'^tutorial', views.stepbystep, name='stepbystep'),
    re_path(r'^publications', views.publications, name='publications'),
    re_path(r'^generateforall', views.generateforall_view, name='generateforall'),
    re_path(r'^get_bundle', views.get_bundle, name='get_bundle'),
    re_path(r'^about', views.about, name='about'),
    re_path(r'^api/', include(api_urls)),
    re_path(r'^progress', views.progress_page),
    re_path(r'500', views.handler500),
    re_path(r'faqs', views.faqs, name="faqs"),
    re_path(r'get_branches', views.get_branches),
    re_path(r'get_outline', views.get_outline),
    re_path(r'^show_repos_list', views.show_repos_list),
    re_path(r'^get_repos_list_file', views.get_repos_list_file),
    re_path(r'^publish', views.publish_view),
    re_path(r'^delete_published', views.delete_published),
    re_path(r'^update_stats', views.update_stats_view),
    re_path(r'^syntax', views.syntax_check_view),
    re_path(r'^status', views.status_view),
    re_path(r'show_stats', views.show_stats),
    re_path(r'', views.home_view, name='home')
]

handler500 = 'OnToology.views.handler500'


if settings.DEBUG:
    from django.contrib import admin
    from django.urls import path
    from django.conf.urls.static import static
    # old media url
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = [path('admin/', admin.site.urls)] + urlpatterns
