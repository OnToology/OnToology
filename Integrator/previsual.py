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

from subprocess import call
import os
# import OnToology
from . import dolog
import random
import string


ToolUser = 'OnToologyUser'
ToolEmail = 'ontoology@delicias.dia.fi.upm.es'
previsual_dir = os.environ['previsual_dir']

temp_dir = os.environ['github_repos_dir']


def start_previsual(repo_dir, target_repo):
    """
        repo_dir: is absolute repository dir e.g. '/home/.../targetrepo'
        target_repo: as text
    """
    generate_previsual(repo_dir, target_repo)


def generate_previsual(repo_dir, target_repo):
    """
        repo_dir: is absolute repository dir e.g. '/home/.../targetrepo'
        target_repo : user/reponame

    """
    repo_name = target_repo.split('/')[-1]
    temp_previsual_folder_dir = generate_previsual_page(repo_dir, repo_name)
    # Create branch for Github pages
    branch_name = 'gh-pages'
    from_branch_name = 'master'
    comm = "cd "+repo_dir
    comm += ";git branch -D "+branch_name
    comm += ";git checkout --orphan "+branch_name
    comm += ";git rm -rf ."
    call(comm, shell=True)
    comm = 'cp -Rf %s/* %s ;' % (temp_previsual_folder_dir, repo_dir)
    dolog('comm: '+comm)
    call(comm, shell=True)
    comm = "cd "+repo_dir
    comm += ';git config user.email "%s"' % ToolEmail
    comm += ';git config user.name "%s"' % ToolUser
    comm += ';git add .'
    comm += ';git commit -m "ontoology generated"'
    comm += ";git push -f origin "+branch_name
    dolog('will call: '+comm)
    call(comm, shell=True)


def generate_previsual_page(repo_dir_folder, repo_name):
    """
    :param repo_dir_folder: absolute target repo dir
    :param repo_name: just the repo name
    :return: the abs dir of the temp folder where the previsualization is located in
    """
    # delete OnToology folder before generating the previsualization
    # because it contains ontologies that will show in the previsualization page
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
    sec = 'doc-prev-'+sec
    repo_parent_folder, t = os.path.split(repo_dir_folder)
    if t=='':
        repo_parent_folder = os.path.split(repo_dir_folder[:-1])
    comm = "mv %s %s" % (os.path.join(repo_dir_folder, 'OnToology'), repo_parent_folder) # should be moved back after vocablite generates the page
    # comm = "rm -Rf %s" % os.path.join(repo_dir_folder, 'OnToology')
    dolog('comm: '+comm)
    call(comm, shell=True)
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
    sec = 'prev-'+sec
    temp_folder = os.path.join(temp_dir, sec)
    comm = "java -jar %s -i %s -o %s -n %s" % \
           (os.path.join(previsual_dir, "vocabLite-1.0-jar-with-dependencies.jar"), repo_dir_folder, temp_folder,
            repo_name)
    dolog('comm: '+comm)
    call(comm, shell=True)
    return temp_folder


def get_confs_from_local(repo_abs_dir):
    """
        repo_abs_dir: abs dir for the repo
        return list ontology relative dirs
    """
    ont_files = []
    if repo_abs_dir[-1] == os.sep:
        repo_abs_dir = repo_abs_dir[:-1]
    num_of_parent_dirs = len(full_path_split(repo_abs_dir))
    dolog("searching for ont in %s" % repo_abs_dir)
    for root, dirs, files in os.walk(repo_abs_dir, topdown=False):
        for name in files:
            file_abs_dir = os.path.join(root, name)
            if 'OnToology.cfg' in file_abs_dir:
                parent_folder = os.path.split(file_abs_dir)[0]
                doc_file = os.path.join(parent_folder, 'documentation', 'index.html')
                if os.path.exists(doc_file):
                    ont = full_path_split(parent_folder)[num_of_parent_dirs:]
                    ont = os.path.join(*ont)
                    ont_files.append(ont)
    dolog('There are %d ontologies' % len(ont_files))
    for o in ont_files:
        print o
    return ont_files


def full_path_split(dir):
    t = os.path.split(dir)
    if t[0] == "":
        return [t[1]]
    if t[1] == "" and t[0] == os.path.sep:
        return [t[0]]
    if t[1].strip() == "":
        return full_path_split(t[0])
    return full_path_split(t[0]) + [t[1]]

