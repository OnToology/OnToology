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
from OnToology import api_views as views
from django.conf import settings

urlpatterns = patterns('',
    # url(r'^admin', views.superadmin, name='superadmin'),
    url(r'home', views.home),
    url(r'', views.home, name='home'),
)
