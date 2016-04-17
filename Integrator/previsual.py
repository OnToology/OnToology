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

ToolUser = 'OnToologyUser'
ToolEmail = 'ahmad88csc@gmail.com'


def start_previsual(repo_dir,target_repo):
    """
        repo_dir: is absolute repository dir e.g. '/home/.../targetrepo'
        target_repo: as text
    """
    ontologies_dirs = prep(target_repo,repo_dir)
    generate_previsual(repo_dir, ontologies_dirs)


def generate_previsual(repo_dir,ontologies_dir):
    """
        repo_dir: is absolute repository dir e.g. '/home/.../targetrepo'
        ontologies_dir: a list of relative ontologies dir inside OnToology folder e.g.
            [ 'OnToology/org/daniel.owl',...
            ] 
    """
    #Create branch for Github pages
    branch_name = 'gh-pages'
    from_branch_name = 'master'
    comm = "cd "+repo_dir
    comm += ";git branch -D "+branch_name
    comm += ";git checkout --orphan "+branch_name
    comm += " ;git rm -rf ."
    links = []
    for ontology_dir in ontologies_dir:
        doc_dir = os.path.join(ontology_dir,'documentation')
        links.append(os.path.join(doc_dir,'index.html'))
        comm += ";git checkout "+from_branch_name+" "+os.path.join(doc_dir,'index.html')
        comm += ";git checkout "+from_branch_name+" "+os.path.join(doc_dir,'provenance')
        comm += ";git checkout "+from_branch_name+" "+os.path.join(doc_dir,'resources')
        comm += ";git checkout "+from_branch_name+" "+os.path.join(doc_dir,'sections')
    print("will call: "+comm)
    call(comm, shell=True)
    main_index_file = os.path.join(repo_dir, 'index.html')
    f = open(main_index_file, 'w')
    print("opened file: "+f.name)
    f.write(get_main_index(links))
    print("after writing into the file")
    print(get_main_index(links))
    f.close()
    comm = "cd "+repo_dir
    comm += ';git config user.email "%s"' % ToolEmail
    comm += ';git config user.name "%s"' % ToolUser
    comm += ';git add .'
    comm += ';git commit -m "ontoology generated"'
    comm += ";git push -f origin "+branch_name  # git push -f origin branch
    print('will call: '+comm)
    call(comm, shell=True)
    

def get_main_index(links):
    links_html=""
    for i, l in enumerate(links, start=1):
        name = l.split('/')[-3]  # get the file name from blah/blah/filename.someext/documentation/index.html
        name = (name.split('.')[:-1])[0] # get file name without the file extension
        links_html += "<tr class='highl'><td>%d</td><td><a class='darktext' href='%s'>%s</a></td></tr>" % (i, l, name)
        # links_html+= "<li class='btn btn-default highl'><a class='darktext' href='%s'>%s</a></li><br><br>"%(l,l)
    html = """
        <html>
            <head>
                <title>OnToology prevision documentation list</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap-theme.min.css">
                <link rel="stylesheet" href="http://getbootstrap.com/examples/cover/cover.css">
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
               <style>
                    .darktext{color: #333333;}    
                   .highl{background-color: #FBFBFB; color: #333333;}
               </style>
            </head>
            <body><br><br>
                <div class="container-fluid">
                    <div class="table-responsive col-md-offset-2  col-md-8">
                        <table class="table table-striped">
                            <tr>
                                <td>#</td> <td>URL to documentation</td>
                            </tr>
                        %s
                        </table>
                    </div>
                </div>
            </body>
        </html>
    """%(links_html)
    return html


def prep(target_repo,repo_dir):
    """
        target_repo: as text
        return list of ontologies dir under OnToology e.g. ['OnToology/daniel.owl',...]
    """
    ontologies_dirs = []
    # The below line is to get ont_files from a master repo from github
    # repo, ont_files = OnToology.autoncore.get_confs_from_repo(target_repo)
    # The below like is to get ont_files from a local repo instead
    ont_files = get_confs_from_local(repo_dir)
    for ofi in ont_files:
        owl_abs = os.path.join(repo_dir,ofi,'documentation','index.html')
        if os.path.exists(owl_abs):
            ontologies_dirs.append(ofi)
            print("***************************************")
            print("found is: "+ofi)
        else:
            print("not found is: "+ofi)
            print("full dir: "+owl_abs)
    return ontologies_dirs


def get_confs_from_local(repo_abs_dir):
    """
        repo_abs_dir: abs dir for the repo
        return list ontology relative dirs
    """
    ont_files = []
    if repo_abs_dir[-1] == os.sep:
        repo_abs_dir = repo_abs_dir[:-1]
    num_of_parent_dirs = len(full_path_split(repo_abs_dir))
    print("searching for ont in %s"%(repo_abs_dir))
    for root, dirs, files in os.walk(repo_abs_dir, topdown=False):
        for name in files:
            file_abs_dir = os.path.join(root, name)
            if 'OnToology.cfg' in file_abs_dir:
                parent_folder = os.path.split(file_abs_dir)[0]
                doc_file = os.path.join(parent_folder,'documentation','index.html')
                if os.path.exists(doc_file):
                    ont = full_path_split(parent_folder)[num_of_parent_dirs:]
                    ont = os.path.join(*ont)
                    ont_files.append(ont)
            # print(os.path.join(root, name))
    print 'There are %d ontologies'%(len(ont_files))
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
    
    
# start_previsual('/Users/blakxu/test123/pro/target','ahmad88me/target')
        
# generate_previsual('/Users/blakxu/test123/pro/target',['OnToology/org/daniel.owl'])

if __name__ == "__main__":
    print "autoncore command: "+str(sys.argv)
    if use_database:
        connect('OnToology')
    git_magic(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4:])



