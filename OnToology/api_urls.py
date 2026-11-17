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
from OnToology import api_views as views

urlpatterns = [
    re_path(r'login', views.login),
    re_path(r'repos$', views.ReposView.as_view()),  # for add and list
    re_path(r'repos/$', views.ReposView.as_view()),  # for add and list
    re_path(r'repos/(?P<repoid>\w+)', views.ReposView.as_view()),  # for the delete
    re_path(r'generate_all', views.generate_all),
    re_path(r'publishnames', views.PublishView.as_view()),
]
