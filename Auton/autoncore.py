#!/usr/bin/python
import sys, os
from github import Github
from datetime import datetime
from subprocess import call
import string, random
import time
from setuptools.command.setopt import config_file








parent_folder = None
ar2dtool_config_types = ['ar2dtool-taxonomy.conf','ar2dtool-class.conf']
ar2dtool_config = os.environ['ar2dtool_config']
#e.g. ar2dtool_dir = 'blahblah/ar2dtool/bin/'
ar2dtool_dir = os.environ['ar2dtool_dir']
#e.g. home = 'blahblah/temp/'
home = os.environ['github_repos_dir']

sleeping_time = 7

ontology_formats = ['.rdf','.owl','.ttl']

g = None

log_file_dir = None#'&1'#which is stdout #sys.stdout#by default

def git_magic(target_repo,user,cloning_repo,changed_files):
    global g
    global parent_folder
    parent_folder = user
#    pid = os.fork()
#     if pid>0:# if parent
#         print 'parent will return'
#         return
# #     f = open(build_file_structure(user+'.log','logs'), 'w')
# #     sys.stdout = f
#     else:
#         print 'this is child'

#     f = open(build_file_structure(user+'.log','logs'), 'w')
#     sys.stdout = f
    prepare_log(user)
    print str(datetime.today())
    print '############################### magic #############################'
    #so the tool user can takeover and do stuff
    username = os.environ['github_username']
    password = os.environ['github_password']
    g = Github(username,password)    
    local_repo = target_repo.replace(target_repo.split('/')[-2] ,'AutonUser')
    delete_repo(local_repo)
    #print 'repo deleted'
    fork_repo(target_repo,username,password)
    print 'repo forked'
    clone_repo(cloning_repo,user)
    print 'repo cloned'
#     update_readme(changed_files,cloning_repo,user)
#     print 'readme updated'
    auton_conf = get_auton_configuration()
    print str(auton_conf)
    if auton_conf['ar2dtool_enable']:
        print 'ar2dtool_enable is true'
        draw_diagrams(changed_files)
        print 'diagrams drawn'
    else: 
        print 'ar2dtool_enable is false'
    if auton_conf['widoco_enable']:
        print  'widoco_enable is true'
        generate_widoco_docs(changed_files)
        print 'generated docs'
    else:
        print  'widoco_enable is false'
    if auton_conf['oops_enable']:
        print 'oops_enable is true'
        oops_ont_files(target_repo,changed_files)
        print 'oops checked ontology for pitfalls'
    else:
        print 'oops_enable is false'
    commit_changes()
    print 'changes committed'
    remove_old_pull_requests(target_repo)
    r = send_pull_request(target_repo,'AutonUser')
    print 'pull request is sent'
    #return r



def prepare_log(user):
    global log_file_dir
    file_dir = build_file_structure(user+'.log', 'log', home)
    f = open(file_dir,'w')
    sys.stdout=f
    log_file_dir = file_dir
    
    

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
    comm+= ' > "'+log_file_dir+'"'
    call(comm,shell=True)
    print 'fork'
    
    


def clone_repo(cloning_repo,user):
    time.sleep(sleeping_time)#the wait time to give github sometime so the repo can be cloned
    comm =  "rm"," -Rf "+home+parent_folder
    print 'type of log_file_dir'+str(type(log_file_dir))
    comm+= ' > "'+log_file_dir+'"'
    print comm
    call(comm, shell=True)
    comm = "git"+" clone"+" "+cloning_repo+" "+home+parent_folder
    comm+= ' > "'+log_file_dir+'"'
    print comm
    call(comm, shell=True)
    comm =  "chmod 777 -R "+home+parent_folder
    comm+= ' > "'+log_file_dir+'"'
    print comm
    call(comm, shell=True)



                
# def update_readme(changed_files,cloning_repo,user):
#     #for i in range(3):
#     try:
#         f = open(home+parent_folder+"/"+"README.md","a")
#         break
#     except IOError:
#         print 'error opening the README file'
#         #print 'readme is not ready: '+str(i)
#         time.sleep(sleeping_time)
#         clone_repo(cloning_repo,user)
#     f.write("\n##Changelog "+str(datetime.today())+"\n")
#     for chf in changed_files:
#         f.write("\n* "+chf)                
#     f.close()
                




def commit_changes():
    gu = ""
    gu = "git config  user.email \"ahmad88csc@gmail.com\";"
    gu+="git config  user.name \"AutonUser\" ;"
    #print "command: "+"cd "+home+parent_folder+";"+gu+" git add README.md "    
    #call("cd "+home+parent_folder+";"+gu+" git add README.md ",shell=True)
    comm =  "cd "+home+parent_folder+";"+gu+" git add . "    
    comm+= ' > "'+log_file_dir+'"'
    print comm
    call(comm,shell=True)
    comm = "cd "+home+parent_folder+";"+gu+" git commit -m 'automated change' "
    comm+= ' > "'+log_file_dir+'"'
    print comm
    call(comm,shell=True)
    gup =""
    gup = "git config push.default matching;"
    comm =  "cd "+home+parent_folder+";"+gu+gup+" git push "
    comm+= ' > "'+log_file_dir+'"'
    print comm
    call(comm,shell=True)







def refresh_repo(target_repo):
    local_repo = target_repo.split('/')[-1]
    g.get_user().get_repo(local_repo).delete()
    g.get_user().create_fork(target_repo)




def remove_old_pull_requests(target_repo):
    title = 'AutonTool update'
    for p in g.get_repo(target_repo).get_pulls():
        if p.title == title:
            p.edit(state="closed")
    



def send_pull_request(target_repo,username):
    title = 'AutonTool update'
    body = title
    err = ""
#    for i in range(3):
    time.sleep(sleeping_time)
    try:
        g.get_repo(target_repo).create_pull(head=username+':master',base='master',title=title,body=body)
        #return 'pull request created successfully'
        return {'status': True, 'msg':'pull request created successfully' }
    except Exception as e:
        err = str(e.data)
        print 'pull request error: '+err
        #print 'pull('+str(i)+'): '+err

    #return err
    return {'status': False, 'error': err}



def webhook_access(client_id,redirect_url):
    scope = 'admin:org_hook'
    scope+=',admin:org,admin:public_key,admin:repo_hook,gist,notifications,delete_repo,repo_deployment,repo,public_repo,user,admin:public_key'
    sec = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(9)])
    return "https://github.com/login/oauth/authorize?client_id="+client_id+"&redirect_uri="+redirect_url+"&scope="+scope+"&state="+sec, sec






def add_webhook(target_repo,notification_url):
    name = "web"
    active = True
    events = ["push"]
    config = {
               "url": notification_url,
               "content_type": "form"
    }
    try:
        g.get_repo(target_repo).create_hook(name,config,events,active)
        return {'status': True}
    except Exception as e:
        return {'status': False, 'error': e.data}



def add_collaborator(target_repo,user):
    try:
        msg = g.get_repo(target_repo).add_to_collaborators(user)
        return {'status': True, 'msg': str(msg) }
    except Exception as e:
        return {'status': False, 'error': e.data}



def update_g(token):
    global g
    g = Github(token)



##########################~~~~~~~~~~~~##################################
##########################  ar2dtool   #################################
##########################~~~~~~~~~~~~~#################################



def draw_diagrams(rdf_files):
    print str(len(rdf_files))+' changed files'
    for r in rdf_files:
        #print r+' is changed '
        if r[-4:] in ontology_formats:
            for t in ar2dtool_config_types:
                draw_file(r,t)
        else:
            pass
            #print r+' is not an rdf'




def get_ar2dtool_config(config_type):
    f = open(ar2dtool_config+'/'+config_type,"r")
    return f.read()






def draw_file(rdf_file,config_type):
    outtype="png"
    abs_dir = home+parent_folder+'/'+'drawings'+'/'+config_type+'/'
    config_file = abs_dir+config_type
    directory = ""
    if len(rdf_file.split('/'))>1:
        directory = '/'.join(rdf_file.split('/')[0:-1])
        if not os.path.exists(abs_dir+directory):
            os.makedirs(abs_dir+directory)
    try:
        open(config_file,"r")
    except IOError:
        if not os.path.exists(abs_dir):
            os.makedirs(abs_dir)
        f = open(config_file,"w")
        f.write(get_ar2dtool_config(config_type))
        f.close()
    except Exception as e:
        print 'in draw_file: exception opening the file: '+str(e)
    comm = 'java -jar '
    comm+= ar2dtool_dir+'ar2dtool.jar -i '
    comm+= home+parent_folder+'/'+rdf_file+' -o '
    comm+= abs_dir+rdf_file+'.'+outtype+' -t '+outtype+' -c '+config_file+' -GV -gml '
    comm+= ' > "'+log_file_dir+'"'
    print comm
    call(comm,shell=True)
# draw_file('myrdfs/sample.rdf')



########################################################################
############################# Widoco ###################################
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
    abs_dir = home+parent_folder+'/'+'docs'+'/'
    config_file = abs_dir+rdf_file.split('/')[-1]+'.widoco.conf'
    directory = ""
    if len(rdf_file.split('/'))>1:
        directory = '/'.join(rdf_file.split('/')[0:-1])
        if not os.path.exists(abs_dir+directory):
            os.makedirs(abs_dir+directory)
    try:
        open(config_file,"r")
    except IOError:
        if not os.path.exists(abs_dir):
            os.makedirs(abs_dir)
        f = open(config_file,"w")
        f.write(get_widoco_config())
        f.close()
    except Exception as e:
        print 'in create_widoco_doc: exception opening the file: '+str(e)
    comm = "cd "+home+parent_folder+"; "
    comm+= "java -jar "
    comm+=widoco_dir+"widoco-0.0.1-jar-with-dependencies.jar "
    comm+=" -ontFile "+home+parent_folder+'/'+rdf_file
    comm+=" -outFolder "+abs_dir+directory
    comm+=" -confFile "+config_file
    print comm
    call(comm,shell=True)
    


########################################################################
######################  Auton configuration file  ######################
########################################################################



import ConfigParser

def get_auton_configuration():
    print 'auton config is called'
    config = ConfigParser.RawConfigParser()
    ar2dtool_sec_name = 'ar2dtool'
    widoco_sec_name = 'widoco'
    oops_sec_name = 'oops'
    ar2dtool_enable = True
    widoco_enable = True
    oops_enable = True
    opened_conf_files = config.read(home+parent_folder+'/auton.cfg')
    if len(opened_conf_files) == 1:
        print 'auton configuration file exists'
        print opened_conf_files[0]
        try:
            ar2dtool_enable = config.getboolean(ar2dtool_sec_name,'enable')
            print 'got ar2dtool enable value'
        except:
            print 'ar2dtool enable value doesnot exist'
            pass
        try:
            widoco_enable = config.getboolean(widoco_sec_name, 'enable')
            print 'got widoco enable value'
        except:
            print 'widoco enable value doesnot exist'
            pass
        try:
            oops_enable = config.getboolean(oops_sec_name, 'enable')
            print 'got oops enable value'
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
        conff = home+parent_folder+'/auton.cfg'
        print 'will create conf file: '+ conff
        try:
            with open(conff, 'wb') as configfile:
                config.write(configfile)
        except Exception as e:
            print 'expection: '
            print e
    return {'ar2dtool_enable':ar2dtool_enable , 'widoco_enable': widoco_enable, 'oops_enable': oops_enable}




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
#     req = urllib2.Request(url, xml_content)
#     req.add_header('Content-Type', 'application/xml; charset=utf-8')
#     req.add_header('Content-Length', len(xml_content))
#     oops_reply = urllib2.urlopen(req)
#     oops_reply = oops_reply.read()
    #print 'OOPS! reply:  '+oops_reply
    headers = {'Content-Type': 'application/xml', 
               'Connection': 'Keep-Alive',
               'Content-Length':len(xml_content),
                
                'Accept-Charset': 'utf-8'
                }
    oops_reply = requests.post(url, data=xml_content, headers=headers)
    oops_reply = oops_reply.text
    print 'got oops reply'#+oops_reply 
    issues_s = output_parsed_pitfalls(ont_file,oops_reply)
    close_old_oops_issues_in_github(target_repo)
    create_oops_issue_in_github(target_repo, issues_s)





def output_raw_pitfalls(ont_file,oops_reply):
    ont_file_abs_path = build_file_structure(ont_file+'.oops', 'oops')
    f = open(ont_file_abs_path,'w')
    f.write(oops_reply)
    f.close()
    print 'oops file written'






def output_parsed_pitfalls(ont_file,oops_reply):
    ont_file_abs_path = build_file_structure(ont_file+'.oops', 'oops')
    f = open(ont_file_abs_path,'w')
    issues, interesting_features = parse_oops_issues(oops_reply)
    s= ""
    #print str(issues)
    for i in issues:
        for intfea in interesting_features:
            if intfea in issues[i]:
                val = issues[i][intfea].split('^^')[0]
                key = intfea.split("#")[-1].replace('>','')
                s+=key+": "+val+"\n"
        s+"\n"
        s+=20*"="
        s+="\n"
    f.write(s)
    f.close()
    print 'oops file written'
    return s



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




def create_oops_issue_in_github(target_repo,oops_issues):
    print 'will create an oops issue'
    try:
        g.get_repo(target_repo).create_issue('OOPS', oops_issues)
    except Exception as e:
        print 'exception when creating issue: '+e.data
        
    


def close_old_oops_issues_in_github(target_repo):
    print 'will close old issues'
    for i in g.get_repo(target_repo).get_issues(state='open'):
        if i.title=='OOPS':
            i.edit(state='closed')






# def get_pitfalls(ont_file):
#     
# import urllib2
# ont_file = 'daniel.owl'
# ont_file_full_path = ont_file#get_abs_path(ont_file)
# f = open(ont_file_full_path,'r')
# ont_file_content = f.read()
# url = 'http://oops-ws.oeg-upm.net/rest'
# xml_content = """
# <?xml version="1.0" encoding="UTF-8"?>
# <OOPSRequest>
#       <OntologyUrl></OntologyUrl>
#       <OntologyContent>%s</OntologyContent>
#       <Pitfalls></Pitfalls>
#       <OutputFormat></OutputFormat>
# </OOPSRequest>    
# """ %(ont_file_content)
# req = urllib2.Request(url, xml_content)
# req.add_header('Content-Type', 'application/xml; charset=utf-8')
# req.add_header('Content-Length', len(xml_content))
# req.add_header("Accept" , "*/*")
# 
# req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36')
# 
# 
# 
# oops_reply = urllib2.urlopen(req)
# oops_reply = oops_reply.read()
# print 'OOPS! reply:  '+oops_reply
    



# 
#  
# import requests
# import json 
#  
# ont_file = 'daniel.owl'
# ont_file_full_path = ont_file#get_abs_path(ont_file)
# f = open(ont_file_full_path,'r')
# ont_file_content = f.read()
# url = 'http://oops-ws.oeg-upm.net/rest'
# xml_content = """
# <?xml version="1.0" encoding="UTF-8"?>
# <OOPSRequest>
#       <OntologyUrl></OntologyUrl>
#       <OntologyContent>%s</OntologyContent>
#       <Pitfalls></Pitfalls>
#       <OutputFormat></OutputFormat>
# </OOPSRequest>    
# """ %(ont_file_content)
#   
# headers = {'Content-Type': 'application/xml', 
#            'Connection': 'Keep-Alive',
#            'Content-Length':len(xml_content),
#             
#             'Accept-Charset': 'utf-8'
#             }
#  
# oops_reply = requests.post(url, data=xml_content, headers=headers)
# oops_reply = oops_reply.text
#  
# 
#  
# oops_reply = json.loads(oops_reply)["data"]






#############################################################################################
################################# generic helper functions ##################################
#############################################################################################




def valid_ont_file(r):
    if r[-4:] in ontology_formats:
        return True 
    return False




def get_abs_path(relative_path):
    return home+parent_folder+'/'+relative_path




def get_parent_path(f):
    return '/'.join(f.split('/')[0:-1])




def build_file_structure(file_with_rel_dir,category_folder='',abs_home=''):#e.g. category_folder = docs, file_with_rel_dir = ahmad88me/org/ont.txt
    if abs_home=='':
        abs_dir = get_abs_path('')
    else:
        abs_dir=abs_home
    if category_folder!='':
        abs_dir+=category_folder+'/'
    abs_dir_with_file= abs_dir+file_with_rel_dir
    abs_dir = get_parent_path(abs_dir_with_file)
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    return abs_dir_with_file



if __name__ == "__main__":
    print "autoncore command: "+str(sys.argv)
    git_magic(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4:])







