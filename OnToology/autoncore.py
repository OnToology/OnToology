#!/usr/bin/python
import sys, os
from github import Github
from datetime import datetime
from subprocess import call
import string, random
import time
import StringIO

import settings

import shutil

# from models import Repo

from mongoengine import *

use_database = True

ToolUser = 'OnToologyUser'

sys.stdout = sys.stderr
default_stdout = sys.stderr
default_stderr = sys.stderr

parent_folder = None
ar2dtool_config_types = ['ar2dtool-taxonomy.conf','ar2dtool-class.conf']
ar2dtool_config = os.environ['ar2dtool_config']
#e.g. ar2dtool_dir = 'blahblah/ar2dtool/bin/'
ar2dtool_dir = os.environ['ar2dtool_dir']
#e.g. home = 'blahblah/temp/'
home = os.environ['github_repos_dir']

verification_log_fname='verification.log'


sleeping_time = 7

ontology_formats = ['.rdf','.owl','.ttl']

g = None

log_file_dir = None #'&1'#which is stdout #sys.stdout#by default

tools_conf = {
           'ar2dtool': { 'folder_name': 'diagrams',  
                        'type': 'png'
                        },
            'widoco': { 'folder_name': 'documentation' 
                       },
            'oops': {'folder_name' : 'evaluation'}
}




def git_magic(target_repo,user,cloning_repo,changed_filesss):
    global g
    global parent_folder
    parent_folder = user
    if not settings.TEST:
        prepare_log(user)
    print str(datetime.today())
    print '############################### magic #############################'
    print 'target_repo: '+target_repo
    change_status(target_repo,'Preparing')
    #so the tool user can takeover and do stuff
    username = os.environ['github_username']
    password = os.environ['github_password']
    g = Github(username,password)    
    local_repo = target_repo.replace(target_repo.split('/')[-2] ,ToolUser)
    if not settings.TEST or not settings.test_conf['local']:
        delete_repo(local_repo)
    #print 'repo deleted'
    if not settings.TEST or not settings.test_conf['local']:
        change_status(target_repo, 'forking repo')
        fork_repo(target_repo,username,password)
        print 'repo forked'
    if not settings.TEST or not settings.test_conf['local']:
        change_status(target_repo,'cloning repo')
        clone_repo(cloning_repo,user)
        print 'repo cloned'
    files_to_verify=[]
    for chf in changed_filesss:
        auton_conf = {'ar2dtool_enable':False , 'widoco_enable': False, 'oops_enable': False}
        if chf[-4:] not in ontology_formats: #validate ontology formats
            if get_file_from_path(chf) =='OnToology.cfg':
                print 'OnToology.cfg is changed'
                fi = get_level_up(chf)
                fi = fi[6:]
                print 'ont file is: '+fi
                changed_files = [fi]
                auton_conf = get_auton_configuration(fi)
            elif get_file_from_path(chf) in ar2dtool_config_types:
                auton_conf['ar2dtool_enable'] = True
                fi = get_level_up(chf)
                fi = get_level_up(fi)
                fi = get_level_up(fi)
                fi = fi[6:]
                changed_files = [fi]
            elif  'widoco.conf' in  get_file_from_path(chf):
                fi = get_level_up(chf)
                fi = get_level_up(fi)
                fi = fi[6:]
                changed_files = [fi]
        else:
            print 'working with: '+chf
            changed_files = [chf]
            auton_conf = get_auton_configuration(chf)
            #The below three lines is to add files to verify their output later on
            ftvcomp = auton_conf
            ftvcomp['file'] = chf
            files_to_verify.append(ftvcomp)
        print str(auton_conf)
        exception_if_exists = ""
        if auton_conf['ar2dtool_enable']:
            print 'ar2dtool_enable is true'
            change_status(target_repo,'drawing diagrams')
            try:
                draw_diagrams(changed_files)
                print 'diagrams drawn successfully'

            except Exception as e:
                exception_if_exists+=chf+": "+str(e)+"\n"
                print 'diagrams not drawn: '+str(e)
        else: 
            print 'ar2dtool_enable is false'
        if auton_conf['widoco_enable']:
            print  'widoco_enable is true'
            change_status(target_repo, 'generating documents')
            try:
                generate_widoco_docs(changed_files)
            except Exception as e:
                exception_if_exists+=str(e)
            print 'generated docs'
        else:
            print  'widoco_enable is false'
        if auton_conf['oops_enable']:
            print 'oops_enable is true'
            change_status(target_repo, 'OOPS is checking for errors')
            try:
                oops_ont_files(target_repo,changed_files)
            except Exception as e:
                exception_if_exists+=str(e)
            print 'oops checked ontology for pitfalls'
        else:
            print 'oops_enable is false'
    if not settings.TEST or not settings.test_conf['local']:
        commit_changes()
        print 'changes committed'
        remove_old_pull_requests(target_repo)
    if exception_if_exists=="": #no errors
        change_status(target_repo, 'validating')
    else:
        change_status(target_repo, exception_if_exists)
    print 'will generate user log'
    generate_user_log(parent_folder+'.log')
    #return r
    for f in files_to_verify:
        repo=None
        if use_database:
            from models import Repo
            repo = Repo.objects.get(url=target_repo)
        verify_tools_generation_when_ready(f, repo)

    if use_database:
        if Repo.objects.get(url=target_repo).state!='validating':
            r = Repo.objects.get(url=target_repo)
            s = r.state
            s = s.replace('validating','')
            r.state = s 
            r.save()
            return 

    if not settings.TEST or not settings.test_conf['local']:
        change_status(target_repo, 'creating a pull request')
        try:
            r = send_pull_request(target_repo,ToolUser)
        except Exception as e:
            exception_if_exists+=str(e)
        print 'pull request is sent'
    
    change_status(target_repo, 'Ready')


def verify_tools_generation_when_ready(ver_file_comp,repo=None):
    ver_file = os.path.join(get_target_home(),ver_file_comp['file'],verification_log_fname)
    ver_file = get_abs_path(ver_file) 
    print 'ver file: '+ver_file
    if ver_file_comp['ar2dtool_enable'] == ver_file_comp['widoco_enable'] == ver_file_comp['oops_enable'] == False:
        return
    for i in range(20):
        time.sleep(15)
        f = open(ver_file, "r")
        s = f.read()
        f.close()
        if ver_file_comp['ar2dtool_enable'] and 'ar2dtool' not in s:
            continue
        if ver_file_comp['widoco_enable'] and 'widoco' not in s:
            continue
        if ver_file_comp['oops_enable'] and 'oops' not in s:
            continue 
         
        os.remove(ver_file)# the verification file is no longer needed
        return verify_tools_generation(ver_file_comp, repo)
    repo.state=ver_file_comp['file']+' is talking too much time to generate output'
    if settings.TEST:
        assert False, 'Taking too much time for verification'
        
                    
   
def update_file(target_repo,path,message,content):
    global g
    assert False, 'testing error'
    username = os.environ['github_username']
    password = os.environ['github_password']
    if g is None:
        g = Github(username, password)
    gg = Github(username,password)
    repo = g.get_repo(target_repo)    
    print 'will update the file <%s> on repo<%s> with the content <%s>'%(path,target_repo,content) 
    #repo.update_content(path, message, content, committer=gg.get_user())
    file = repo.update_content(path, message, content)
    print '%s has the updated content as <%s>'%(path,file.decoded_content)
    print 'file updated'
    


def verify_tools_generation(ver_file_comp,repo=None):
    #AR2DTool
    if ver_file_comp['ar2dtool_enable']:
        target_file = os.path.join(get_abs_path(get_target_home()),ver_file_comp['file'] ,
          tools_conf['ar2dtool']['folder_name'],ar2dtool_config_types[0][:-5],
          get_file_from_path(ver_file_comp['file'])+"."+tools_conf['ar2dtool']['type']+'.graphml')
        file_exists = os.path.isfile(target_file)
        if repo is not None and not file_exists:
            repo.state+=' The Diagram of the file %s is not generated '%(ver_file_comp['file'])
            repo.save()
        if settings.TEST:
             assert file_exists, 'the file %s is not generated'%(target_file)
        elif not file_exists:
            print 'The Diagram of the file %s is not generated '%(ver_file_comp['file'])
    #Widoco
    if ver_file_comp['widoco_enable']:
        target_file = os.path.join(get_abs_path(get_target_home()),ver_file_comp['file'] ,
          tools_conf['widoco']['folder_name'],
          'index.html')
        file_exists = os.path.isfile(target_file)
        if repo is not None and not file_exists:
            repo.state+=' The Documentation of the file %s if not generated '%(ver_file_comp['file'])
            repo.save()
        if settings.TEST:
             assert file_exists, 'the file %s is not generated'%(target_file)
        elif not file_exists:
            print 'The Documentation of the file %s if not generated '%(ver_file_comp['file'])
    #OOPS
    if ver_file_comp['oops_enable']:
        target_file = os.path.join(get_abs_path(get_target_home()),ver_file_comp['file'] ,
          tools_conf['oops']['folder_name'],
          'oopsEval.html')
        file_exists = os.path.isfile(target_file)
        if repo is not None and not file_exists:
            repo.state+=' The Evaluation report of the file %s if not generated '%(ver_file_comp['file'])
            repo.save()
        if settings.TEST:
             assert file_exists, 'the file %s is not generated'%(target_file)
        elif not file_exists:
            print 'The Evaluation report of the file %s if not generated '%(ver_file_comp['file'])



def prepare_log(user):
    global log_file_dir
    global default_stderr
    global default_stdout
    file_dir = build_file_structure(user+'.log', 'log', home)
    f = open(file_dir,'w')
    sys.stdout.flush()
    sys.stderr.flush()
    sys.stdout=f
    sys.stderr=f
    log_file_dir = file_dir
    return f#, stdout, stderr


def return_default_log():
    sys.stdout.flush()
    sys.stderr.flush()
    sys.stdout=default_stdout
    sys.stderr=default_stderr

    

def delete_repo(local_repo):
    try:
        g.get_repo(local_repo).delete()
        print 'repo deleted '
    except:
        print 'the repo doesn\'t exists [not an error]'





def fork_repo(target_repo,username,password):
    time.sleep(sleeping_time)#the wait time to give github sometime so the repo can be forked successfully
    #this is a workaround and not a proper way to do a fork
    comm = "curl --user \"%s:%s\" --request POST --data \'{}\' https://api.github.com/repos/%s/forks" % (username,password,target_repo)
    if not settings.TEST:
        comm+= ' >> "'+log_file_dir+'"'
    print comm
    call(comm,shell=True)
    print 'fork'
    
    


#def clone_repo(cloning_repo,user):
def clone_repo(cloning_repo,parent_folder,dosleep=True):
    print 'home: %s'%(home)
    print 'parent_folder: %s'%(parent_folder)
    print 'logfile: %s'%(log_file_dir)
    if dosleep:
        time.sleep(sleeping_time)#the wait time to give github sometime so the repo can be cloned
    try:
        comm =  "rm"+" -Rf "+home+parent_folder
        if not settings.TEST:
            comm+= ' >> "'+log_file_dir+'"'
        print comm
        call(comm, shell=True)
    except Exception as e:
        print 'rm failed: '+str(e)
    comm = "git"+" clone"+" "+cloning_repo+" "+home+parent_folder
    if not settings.TEST:
        comm+= ' >> "'+log_file_dir+'"'
    print comm
    call(comm, shell=True)
    comm =  "chmod -R 777 "+home+parent_folder
    if not settings.TEST:
        comm+= ' >> "'+log_file_dir+'"'
    print comm
    call(comm, shell=True)
    return home+parent_folder


            

def commit_changes():
    gu = ""
    gu = "git config  user.email \"ahmad88csc@gmail.com\";"
    gu+='git config  user.name "%s" ;'%(ToolUser)
    #print "command: "+"cd "+home+parent_folder+";"+gu+" git add README.md "    
    #call("cd "+home+parent_folder+";"+gu+" git add README.md ",shell=True)
    comm =  "cd "+home+parent_folder+";"+gu+" git add . "    
    if not settings.TEST:
        comm+= ' >> "'+log_file_dir+'"'
    print comm
    call(comm,shell=True)
    comm = "cd "+home+parent_folder+";"+gu+" git commit -m 'automated change' "
    if not settings.TEST:
        comm+= ' >> "'+log_file_dir+'"'
    print comm
    call(comm,shell=True)
    gup =""
    gup = "git config push.default matching;"
    comm =  "cd "+home+parent_folder+";"+gu+gup+" git push "
    if not settings.TEST:
        comm+= ' >> "'+log_file_dir+'"'
    print comm
    call(comm,shell=True)







def refresh_repo(target_repo):
    local_repo = target_repo.split('/')[-1]
    g.get_user().get_repo(local_repo).delete()
    g.get_user().create_fork(target_repo)






def remove_old_pull_requests(target_repo):
    title = 'OnToology update'
    for p in g.get_repo(target_repo).get_pulls():
        if p.title == title:
            p.edit(state="closed")
    




def send_pull_request(target_repo,username):
    title = 'OnToology update'
    body = title
    err = ""
#    for i in range(3):
    time.sleep(sleeping_time)
    try:
        g.get_repo(target_repo).create_pull(head=username+':master',base='master',title=title,body=body)
        #return 'pull request created successfully'
        return {'status': True, 'msg':'pull request created successfully' }
    except Exception as e:
        err = str(e)#e.data}#str(e.data)
        print 'pull request error: '+err
        #print 'pull('+str(i)+'): '+err
    #return err
    return {'status': False, 'error': err}




def webhook_access(client_id,redirect_url):
    scope = 'admin:org_hook'
    scope+=',admin:org,admin:public_key,admin:repo_hook,gist,notifications,delete_repo,repo_deployment,repo,public_repo,user,admin:public_key'
    sec = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(9)])
    return "https://github.com/login/oauth/authorize?client_id="+client_id+"&redirect_uri="+redirect_url+"&scope="+scope+"&state="+sec, sec

def remove_webhook(target_repo, notification_url):
    global g
    for hook in g.get_repo(target_repo).get_hooks():
        if hook.config["url"] == notification_url:
            hook.delete()

def add_webhook(target_repo,notification_url,newg=None):
    global g
    if newg is None:
        newg = g        
    name = "web"
    active = True
    events = ["push"]
    config = {
               "url": notification_url,
               "content_type": "form"
    }
    try:
        newg.get_repo(target_repo).create_hook(name,config,events,active)
        return {'status': True}
    except Exception as e:
        return {'status': False, 'error': str(e)}#e.data}



def add_collaborator(target_repo,user,newg=None):
    global g
    if newg is None:
        newg = g
    print 'let us try this: '+newg.get_user().email
    try:
        msg = newg.get_repo(target_repo).add_to_collaborators(user)
        return {'status': True, 'msg': str(msg) }
    except Exception as e:
        return {'status': False, 'error': str(e)}#e.data}



def update_g(token):
    global g
    g = Github(token)



##########################~~~~~~~~~~~~##################################
##########################~~~~~~~~~~~~##################################
##########################  ar2dtool   #################################
##########################~~~~~~~~~~~~~#################################
##########################~~~~~~~~~~~~~#################################




def draw_diagrams(rdf_files):
    print str(len(rdf_files))+' changed files'
    for r in rdf_files:
        #print r+' is changed '
        if r[-4:] in ontology_formats:
            for t in ar2dtool_config_types:
                draw_file(r,t) 




def get_ar2dtool_config(config_type):
    f = open(ar2dtool_config+'/'+config_type,"r")
    return f.read()



def draw_file(rdf_file,config_type):
    outtype="png"
    #config_file_abs = build_file_structure(config_type, [get_target_home(),'diagrams',config_type])
    #rdf_file_abs = build_file_structure(rdf_file, [get_target_home(),'diagrams',config_type])    
    
    
    rdf_file_abs = build_file_structure(get_file_from_path(rdf_file),[get_target_home(),rdf_file,'diagrams',config_type[:-5]])
    #now will delete the drawing type folder
    delete_dir(get_parent_path(rdf_file_abs))
    rdf_file_abs = build_file_structure(get_file_from_path(rdf_file),[get_target_home(),rdf_file,'diagrams',config_type[:-5]])
    config_file_abs = build_file_structure(config_type, [get_target_home(),rdf_file,'diagrams','config'])
    try:
        open(config_file_abs,"r")
    except IOError:
        f = open(config_file_abs,"w")
        f.write(get_ar2dtool_config(config_type))
        f.close()
    except Exception as e:
        print 'in draw_file: exception opening the file: '+str(e)
    

        
    comm = 'java -jar '
    comm+= ar2dtool_dir+'ar2dtool.jar -i '
    comm+= get_abs_path(rdf_file)+' -o '
    comm+= rdf_file_abs+'.'+outtype+' -t '+outtype+' -c '+config_file_abs+' -GV -gml '
    if not settings.TEST:
        comm+= ' >> "'+log_file_dir+'"'
    comm+=" ; echo 'ar2dtool' >> "+ os.path.join(get_parent_path(get_parent_path(get_parent_path(rdf_file_abs+'.'+outtype))),verification_log_fname)
    print comm
    call(comm,shell=True)
    #return os.path.isfile(rdf_file_abs+'.gml') 


########################################################################
########################################################################
############################# Widoco ###################################
########################################################################
########################################################################



#e.g. widoco_dir = 'blahblah/Widoco/JAR/'
widoco_dir = os.environ['widoco_dir']
widoco_config = ar2dtool_config+'/'+'widoco.conf'


def get_widoco_config():
    f = open(widoco_config,"r")
    return f.read()



def generate_widoco_docs(changed_files):
    for r in changed_files:
        if r[-4:] in ontology_formats:
            print 'will widoco '+r
            create_widoco_doc(r)
        else:
            pass
            #print r+' does not belong to supported ontology formats for widoco'




def create_widoco_doc(rdf_file):
    print 'in Widoco function'
    rdf_file_abs = get_abs_path(rdf_file)
    #config_file_abs = build_file_structure(rdf_file+'.widoco.conf', [get_target_home(),'documentation'])     
    config_file_abs = build_file_structure(get_file_from_path(rdf_file)+'.widoco.conf', [get_target_home(), rdf_file, 'documentation'])     
    print 'rdf_abs: %s and config_file_abs %s'%(rdf_file_abs,config_file_abs)
    try:
        open(config_file_abs,"r")
    except IOError:
        f = open(config_file_abs,"w")
        f.write(get_widoco_config())
        f.close()
    except Exception as e:
        print 'in create_widoco_doc: exception opening the file: '+str(e)        
    out_abs_dir = get_parent_path(config_file_abs)
    comm = "cd "+get_abs_path('')+"; "
    comm+= "java -jar "
    comm+=' -Dfile.encoding=utf-8 '
    comm+=widoco_dir+"widoco-0.0.1-jar-with-dependencies.jar  -rewriteAll "
    comm+=" -ontFile "+rdf_file_abs
    comm+=" -outFolder "+out_abs_dir
    comm+=" -confFile "+config_file_abs
    if not settings.TEST:
        comm+= ' >> "'+log_file_dir+'" '
    comm+=" ; echo 'widoco' >> "+ os.path.join(get_parent_path(out_abs_dir),verification_log_fname)
    print comm
    call(comm,shell=True)
    
    

########################################################################
########################################################################
######################  Auton configuration file  ######################
########################################################################
########################################################################



import ConfigParser


def get_confs_from_repo(target_repo):
    global g
    repo = g.get_repo(target_repo)
    sha = repo.get_commits()[0].sha
    files = repo.get_git_tree(sha=sha,recursive=True).tree
    conf_files=[]
    for f in files:
        if 'OnToology.cfg' in f.path:
            conf_files.append(f)
    return repo, conf_files




def parse_online_repo_for_ontologies(target_repo):
    repo, conf_paths = get_confs_from_repo(target_repo)
    ontologies=[]
    for cpath in conf_paths:
        file_content = repo.get_file_contents(cpath.path).decoded_content
        #print 'file_content : '+file_content
        buffile = StringIO.StringIO(file_content)
        confs = get_auton_config(buffile)
        #print 'confs: '+str(confs)
        o={}
        #This to only show the relative path on the profile page
        o['ontology'] = get_parent_path(cpath.path)[len(get_target_home()):] #o['ontology'].replace(ontologies_abs_folder,'')
        #o['ontology'] = o['ontology'].replace('/','')
        for c in confs:
            tool = c.replace('_enable','')
            o[tool] = confs[c]
        ontologies.append(o)
    return ontologies




def get_auton_configuration(f=None,abs_folder=None):
    if abs_folder!=None:
        conf_file_abs = os.path.join(abs_folder,'OnToology.cfg')
    elif f != None:
        conf_file_abs = build_file_structure('OnToology.cfg',[get_target_home(),f] )
    else:
        conf_file_abs = build_file_structure('OnToology.cfg',[get_target_home()] )
   
    return get_auton_config(conf_file_abs,from_string=False)    
    
    
def get_auton_config(conf_file_abs,from_string=True):
 

    print 'auton config is called: '
    ar2dtool_sec_name = 'ar2dtool'
    widoco_sec_name = 'widoco'
    oops_sec_name = 'oops'
    ar2dtool_enable = True
    widoco_enable = True
    oops_enable = True
    
    config = ConfigParser.RawConfigParser()
    if from_string:
        opened_conf_files = config.readfp(conf_file_abs)
    else:
        opened_conf_files = config.read(conf_file_abs)
    if from_string or len(opened_conf_files) == 1:
        print 'auton configuration file exists'
        #print opened_conf_files[0]
        try:
            ar2dtool_enable = config.getboolean(ar2dtool_sec_name,'enable')
            print 'got ar2dtool enable value: '+str(ar2dtool_enable)
        except:
            print 'ar2dtool enable value doesnot exist'
            pass
        try:
            widoco_enable = config.getboolean(widoco_sec_name, 'enable')
            print 'got widoco enable value: '+str(widoco_enable)
        except:
            print 'widoco enable value doesnot exist'
            pass
        try:
            oops_enable = config.getboolean(oops_sec_name, 'enable')
            print 'got oops enable value: '+str(oops_enable)
        except:
            print 'oops enable value doesnot exist'
    else:  
        print 'auton configuration file does not exists'
        config.add_section(ar2dtool_sec_name)
        config.set(ar2dtool_sec_name, 'enable', ar2dtool_enable) 
        config.add_section(widoco_sec_name)
        config.set(widoco_sec_name,'enable',widoco_enable)
        config.add_section(oops_sec_name)
        config.set(oops_sec_name,'enable',oops_enable)
        conff = conf_file_abs
        print 'will create conf file: '+ conff
        try:
            with open(conff, 'wb') as configfile:
                config.write(configfile)
        except Exception as e:
            print 'expection: '
            print e
    return {'ar2dtool_enable':ar2dtool_enable , 'widoco_enable': widoco_enable, 'oops_enable': oops_enable}







# def get_auton_configuration(f=None,abs_folder=None):
# #     if f==None:
# #         f=parent_folder 
# #     else:
# #         f=parent_folder+'/'+f
#     print 'auton config is called: '
#     config = ConfigParser.RawConfigParser()
#     ar2dtool_sec_name = 'ar2dtool'
#     widoco_sec_name = 'widoco'
#     oops_sec_name = 'oops'
#     ar2dtool_enable = True
#     widoco_enable = True
#     oops_enable = True
#     if abs_folder!=None:
#         conf_file_abs = os.path.join(abs_folder,'OnToology.cfg')
#     elif f != None:
#         conf_file_abs = build_file_structure('OnToology.cfg',[get_target_home(),f] )
#     else:
#         conf_file_abs = build_file_structure('OnToology.cfg',[get_target_home()] )
#     opened_conf_files = config.read(conf_file_abs)
#     if len(opened_conf_files) == 1:
#         print 'auton configuration file exists'
#         print opened_conf_files[0]
#         try:
#             ar2dtool_enable = config.getboolean(ar2dtool_sec_name,'enable')
#             print 'got ar2dtool enable value: '+str(ar2dtool_enable)
#         except:
#             print 'ar2dtool enable value doesnot exist'
#             pass
#         try:
#             widoco_enable = config.getboolean(widoco_sec_name, 'enable')
#             print 'got widoco enable value: '+str(widoco_enable)
#         except:
#             print 'widoco enable value doesnot exist'
#             pass
#         try:
#             oops_enable = config.getboolean(oops_sec_name, 'enable')
#             print 'got oops enable value: '+str(oops_enable)
#         except:
#             print 'oops enable value doesnot exist'
#     else:  
#         print 'auton configuration file does not exists'
#         config.add_section(ar2dtool_sec_name)
#         config.set(ar2dtool_sec_name, 'enable', ar2dtool_enable) 
#         config.add_section(widoco_sec_name)
#         config.set(widoco_sec_name,'enable',widoco_enable)
#         config.add_section(oops_sec_name)
#         config.set(oops_sec_name,'enable',oops_enable)
#         conff = conf_file_abs
#         print 'will create conf file: '+ conff
#         try:
#             with open(conff, 'wb') as configfile:
#                 config.write(configfile)
#         except Exception as e:
#             print 'expection: '
#             print e
#     return {'ar2dtool_enable':ar2dtool_enable , 'widoco_enable': widoco_enable, 'oops_enable': oops_enable}



########################################################################
############################---------###################################
############################  OOPS!  ###################################
############################\_______/###################################


import requests
import rdfxml


def oops_ont_files(target_repo,changed_files):
    for r in changed_files:
        if valid_ont_file(r):
            print 'will oops: '+r
            get_pitfalls(target_repo,r) 




def get_pitfalls(target_repo,ont_file):
    generate_oops_pitfalls(ont_file)
    if settings.TEST and settings.test_conf['local']:
        return
    ont_file_full_path = get_abs_path(ont_file)
    f = open(ont_file_full_path,'r')
    ont_file_content = f.read()
    url = 'http://oops-ws.oeg-upm.net/rest'
    xml_content = """
    <?xml version="1.0" encoding="UTF-8"?>
    <OOPSRequest>
          <OntologyUrl></OntologyUrl>
          <OntologyContent>%s</OntologyContent>
          <Pitfalls></Pitfalls>
          <OutputFormat></OutputFormat>
    </OOPSRequest>    
    """ %(ont_file_content)
    headers = {'Content-Type': 'application/xml', 
               'Connection': 'Keep-Alive',
               'Content-Length':len(xml_content),
                
                'Accept-Charset': 'utf-8'
                }
    oops_reply = requests.post(url, data=xml_content, headers=headers)
    oops_reply = oops_reply.text
    print 'got oops reply'#+oops_reply 
    issues_s = output_parsed_pitfalls(ont_file,oops_reply)
    close_old_oops_issues_in_github(target_repo,ont_file)
    nicer_issues = nicer_oops_output(issues_s)
    if nicer_issues!="":
        create_oops_issue_in_github(target_repo,ont_file,nicer_issues)
        
    




def output_parsed_pitfalls(ont_file,oops_reply):
    issues, interesting_features = parse_oops_issues(oops_reply)
    s= ""
    for i in issues:
        for intfea in interesting_features:
            if intfea in issues[i]:
                val = issues[i][intfea].split('^^')[0]
                key = intfea.split("#")[-1].replace('>','')
                s+=key+": "+val+"\n"
        s+"\n"
        s+=20*"="
        s+="\n"
    print 'oops issues gotten'
    return s



#generate oops issues using widoco
def generate_oops_pitfalls(ont_file):    
    ont_file_abs_path = get_abs_path(ont_file)
    r = build_file_structure(get_file_from_path(ont_file)+'.'+tools_conf['oops']['folder_name'], [get_target_home(),ont_file,tools_conf['oops']['folder_name']])
    #r = build_file_structure(get_file_from_path(ont_file)+'.oops', [get_target_home(),ont_file,'oops'])
    out_abs_dir = get_parent_path(r)
    comm = "cd "+get_abs_path('')+"; "
    comm+= "java -jar "
    comm+=' -Dfile.encoding=utf-8 '
    comm+=widoco_dir+"widoco-0.0.1-jar-with-dependencies.jar -oops "
    comm+=" -ontFile "+ont_file_abs_path
    comm+=" -outFolder "+out_abs_dir
    #comm+=" -confFile "+config_file_abs
    if not settings.TEST:
        comm+= ' >> "'+log_file_dir+'"'
    comm+=" ; echo 'oops' >> "+ os.path.join(get_parent_path(out_abs_dir),verification_log_fname)
    print comm
    call(comm,shell=True)                 
    shutil.move( os.path.join(out_abs_dir,'OOPSevaluation') , get_parent_path(out_abs_dir))
    shutil.rmtree(out_abs_dir)
    shutil.move(os.path.join(get_parent_path(out_abs_dir),'OOPSevaluation'), out_abs_dir)




def parse_oops_issues(oops_rdf):
    p = rdfxml.parseRDF(oops_rdf)
    raw_oops_list = p.result
    oops_issues={}
    
    #Filter #1
    #Construct combine all data of a single elements into one json like format
    for r in raw_oops_list:
        if r['domain'] not in oops_issues:
            oops_issues[r['domain']] = {}
        oops_issues[r['domain']][r['relation']] = r['range']
    
    #Filter #2
    #get rid of elements without issue id 
    oops_issues_filter2={}
    for  i in oops_issues:
        if '#' not in i:
            oops_issues_filter2[i] = oops_issues[i]
    
    #Filter #3    
    #Only include actual issues (some data are useless to us)
    detailed_desc = []
    oops_issues_filter3={}
    for i in oops_issues_filter2:
        if '<http://www.oeg-upm.net/oops#hasNumberAffectedElements>' in oops_issues_filter2[i]:
            oops_issues_filter3[i] = oops_issues_filter2[i]
                    
    #Filter #4
    #Only include data of interest about the issue
    oops_issues_filter4={}
    issue_interesting_data = [
        '<http://www.oeg-upm.net/oops#hasName>',
        '<http://www.oeg-upm.net/oops#hasCode>',
        '<http://www.oeg-upm.net/oops#hasDescription>',
        '<http://www.oeg-upm.net/oops#hasNumberAffectedElements>',
        '<http://www.oeg-upm.net/oops#hasImportanceLevel>',
        #'<http://www.oeg-upm.net/oops#hasAffectedElement>',
        '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>',
    ]
    for i in oops_issues_filter3:
        oops_issues_filter4[i]={}
        for intda in issue_interesting_data:
            if intda in oops_issues_filter3[i]:
                oops_issues_filter4[i][intda] = oops_issues_filter3[i][intda]
    return oops_issues_filter4, issue_interesting_data




def create_oops_issue_in_github(target_repo,ont_file,oops_issues):
    print 'will create an oops issue'
    try:
        g.get_repo(target_repo).create_issue('OOPS! Evaluation for '+ont_file, oops_issues)
    except Exception as e:
        print 'exception when creating issue: '+str(e)#e.data}#e.data
        
    


def close_old_oops_issues_in_github(target_repo,ont_file):
    print 'will close old issues'
    for i in g.get_repo(target_repo).get_issues(state='open'):
        if i.title == ('OOPS! Evaluation for '+ont_file) :
            i.edit(state='closed')



def nicer_oops_output(issues):
    sugg_flag = '<http://www.oeg-upm.net/oops#suggestion>'
    pitf_flag = '<http://www.oeg-upm.net/oops#pitfall>'
    warn_flag = '<http://www.oeg-upm.net/oops#warning>'
    num_of_suggestions = issues.count(sugg_flag)
    num_of_pitfalls = issues.count(pitf_flag)
    num_of_warnings = issues.count(warn_flag)
    s=" OOPS has encountered %d pitfalls and %d warnings"%(num_of_pitfalls,num_of_warnings)
    if num_of_pitfalls == num_of_suggestions == num_of_warnings ==0:
        return ""
    if num_of_suggestions >0:
        s+="  and have %d suggestions"%(num_of_suggestions)
    nodes = issues.split("====================")
    suggs=[]
    pitfs=[]
    warns=[]
    for node in nodes[:-1]:
        attrs = node.split("\n")
        if sugg_flag in node:
            for attr in attrs:
                if 'hasDescription' in attr:
                    suggs.append(attr.replace('hasDescription: ',''))
                    break
        elif pitf_flag in node :
            for attr in attrs:
                if 'hasName' in attr:
                    pitfs.append(attr.replace('hasName: ',''))
                    break
        elif warn_flag in node:
            for attr in attrs:
                if 'hasName' in attr:
                    warns.append(attr.replace('hasName: ',''))
                    break
        else:
            print 'in nicer_oops_output: strange node: '+node
    if len(pitfs) >0:
        s+="The Pitfalls are the following:\n"
        for i in range(len(pitfs)):
            s+='%d. '%(i+1) + pitfs[i]+"\n"
    if len(warns) >0:
        s+="The Warning are the following:\n"
        for i in range(len(warns)):
            s+="%d. "%(i+1) + warns[i]+"\n"
    if len(suggs) >0:
        s+="The Suggestions are the following:\n"
        for i in range(len(suggs)):
            s+="%d. "%(i+1) + suggs[i]+"\n"
    return s







#############################################################################################
################################# generic helper functions ##################################
#############################################################################################

    


def delete_dir(target_directory):
    comm="rm -Rf "+target_directory
    if not settings.TEST:
        comm += '  >> "'+log_file_dir+'" '
    print comm  
    call(comm,shell=True)


def valid_ont_file(r):
    if r[-4:] in ontology_formats:
        return True 
    return False


def get_target_home():
    return 'OnToology'


def get_abs_path(relative_path):
    return home+parent_folder+'/'+relative_path


def get_level_up(relative_path):
    fi = get_file_from_path(relative_path)
    return relative_path[:-len(fi)-1]


def get_parent_path(f):
    return '/'.join(f.split('/')[0:-1])

def get_file_from_path(f):
    return f.split('/')[-1] 


def build_file_structure(file_with_rel_dir,category_folder='',abs_home=''):#e.g. category_folder = docs, file_with_rel_dir = ahmad88me/org/ont.txt
    if abs_home=='':
        abs_dir = get_abs_path('')
    else:
        abs_dir=abs_home
    if type(category_folder) == type(""):# if string    
        if category_folder!='':
            abs_dir+=category_folder+'/'
    elif type(category_folder) == type([]):# if list
        for catfol in category_folder:
            abs_dir+=catfol+'/'
    abs_dir_with_file= abs_dir+file_with_rel_dir
    abs_dir = get_parent_path(abs_dir_with_file)
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    return abs_dir_with_file





#############################################################################################
################################ Database functions #########################################
#############################################################################################

#if use_database:
#    from Auton.models import Repo
#import it for now
def change_status(target_repo, state):
    from models import Repo
#     class Repo(Document):
#         url = StringField(max_length=100,default='Not set yet')
#         last_used = DateTimeField(default=datetime.now())
#         created_on = DateTimeField(default=datetime.now())
#         monitoring = StringField(max_length=100,default='Not set yet')
#         state = StringField(max_length=50,default='Ready')
#         owner = StringField(max_length=50,default='no')
    
    
    if not use_database:
        return ''
    try:
        repo = Repo.objects.get(url=target_repo)
        repo.last_used = datetime.today()
        repo.state = state
        repo.owner = parent_folder
        repo.save()
    except DoesNotExist:
        repo = Repo()
        repo.url=target_repo
        repo.state = state
        repo.owner = parent_folder
        repo.save()
    except Exception as e:
        print 'database_exception: '+str(e)




#############################################################################################
#####################   Generate user log file  #############################################
#############################################################################################

#just for the development phase 

def generate_user_log(log_file_name):
    comm='cp '+home+'log/'+log_file_name+ '  ' +os.path.join(settings.MEDIA_ROOT,'logs') #' /home/ubuntu/auton/media/logs/'
    print comm
    sys.stdout.flush()
    if sys.stdout == default_stdout:
        print 'Warning: trying to close sys.stdout in generate_user_log function, I am disabling the closing for now'
    
        
    return_default_log()
    call(comm,shell=True)
    




#############################################################################################
####################################   main  ################################################
#############################################################################################



if __name__ == "__main__":
    print "autoncore command: "+str(sys.argv)
    if use_database:
        connect('OnToology')
    git_magic(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4:])







