import os

import requests


from . import dolog, get_file_from_path, tools_conf, build_path, get_target_home, get_parent_path, log_file_dir, g
from . import verification_log_fname
import rdfxml
from . import call_and_get_log

from subprocess import call
import shutil


widoco_dir = os.environ['widoco_dir']


def oops_ont_files(target_repo, changed_files, base_dir):
    results = ""
    for r in changed_files:
        # if valid_ont_file(r): # this is moved to the caller function, we assume here the changed_files are all ont
        dolog('will oops: ' + r)
        results += get_pitfalls(target_repo, r, base_dir)
    return results


def get_pitfalls(target_repo, ont_file, base_dir):
    r = generate_oops_pitfalls(ont_file, base_dir)
    if r != "":  #  in case of an error
        print "error generateing oops pitfalls: "+str(r)
        return r
    # if settings.TEST and settings.test_conf['local']:
    #    return
    ont_file_full_path = os.path.join(base_dir, ont_file)
    f = open(ont_file_full_path, 'r')
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
    """ % (ont_file_content)
    headers = {'Content-Type': 'application/xml',
               'Connection': 'Keep-Alive',
               'Content-Length': len(xml_content),

               'Accept-Charset': 'utf-8'
               }
    dolog("will call oops webservice")
    oops_reply = requests.post(url, data=xml_content, headers=headers)
    dolog("will get oops text reply")
    oops_reply = oops_reply.text
    # dolog('oops reply is: <<' + oops_reply + '>>')
    dolog('<<<end of oops reply>>>')
    if oops_reply[:50] == '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">':
        if '<title>502 Proxy Error</title>' in oops_reply:
            raise Exception('Ontology is too big for OOPS')
        else:
            raise Exception('Generic error from OOPS')
    issues_s = output_parsed_pitfalls(ont_file, oops_reply)
    dolog('got oops issues parsed')
    close_old_oops_issues_in_github(target_repo, ont_file)
    dolog('closed old oops issues in github')
    nicer_issues = nicer_oops_output(issues_s)
    dolog('get nicer issues')
    if nicer_issues != "":
        # evaluation report in this link\n Otherwise the URL won't work\n"
        nicer_issues += "\n Please accept the merge request to see the evaluation report in this link. Otherwise the URL won't work.\n"
        repo = target_repo.split('/')[1]
        user = target_repo.split('/')[0]
        nicer_issues += "https://rawgit.com/" + user + '/' + repo + \
            '/master/OnToology/' + ont_file + '/evaluation/oopsEval.html'
        create_oops_issue_in_github(target_repo, ont_file, nicer_issues)


def output_parsed_pitfalls(ont_file, oops_reply):
    issues, interesting_features = parse_oops_issues(oops_reply)
    s = ""
    for i in issues:
        for intfea in interesting_features:
            if intfea in issues[i]:
                val = issues[i][intfea].split('^^')[0]
                key = intfea.split("#")[-1].replace('>', '')
                s += key + ": " + val + "\n"
        s + "\n"
        s += 20 * "="
        s += "\n"
    dolog('oops issues gotten')
    return s


# generate oops issues using widoco
def generate_oops_pitfalls(ont_file, base_dir):
    ont_file_abs_path = os.path.join(base_dir, ont_file)
    #  r = build_file_structure(get_file_from_path(ont_file) + '.' + tools_conf['oops'][
    #                         'folder_name'], [get_target_home(), ont_file, tools_conf['oops']['folder_name']])
    r = build_path(os.path.join(base_dir, get_target_home(), ont_file, tools_conf['oops']['folder_name'],
                                get_file_from_path(ont_file) + '.' + tools_conf['oops']['folder_name']))
    #r = build_file_structure(
    #    get_file_from_path(ont_file) + '.' + tools_conf['oops']['folder_name'],
    #        [get_target_home(), ont_file, tools_conf['oops']['folder_name']]
    #)
    dolog('r: '+r)
    dolog('ont file abs path: '+ont_file_abs_path)
    out_abs_dir = get_parent_path(r)
    comm = "cd " + base_dir + "; "
    comm += "java -jar "
    comm += ' -Dfile.encoding=utf-8 '
    comm += widoco_dir + "widoco-0.0.1-jar-with-dependencies.jar -oops "
    comm += " -ontFile '" + ont_file_abs_path
    comm += "' -outFolder '" + out_abs_dir + "'"
    # if not settings.TEST:
    if True:
        comm += ' >> "' + log_file_dir + '"'
    # commenting the use of verification log
    # comm += " ; echo 'oops' >> '" + os.path.join(get_parent_path(out_abs_dir), verification_log_fname) + "'"
    dolog(comm)
    # call(comm, shell=True)
    error_msg, msg = call_and_get_log(comm)
    dolog(msg+error_msg)
    if error_msg != "":
        return "Error while generating the Evaluation"
    dolog("moving1: <%s> to <%s>" % (os.path.join(out_abs_dir, 'OOPSevaluation'), get_parent_path(out_abs_dir)))
    shutil.move(os.path.join(out_abs_dir, 'OOPSevaluation'), get_parent_path(out_abs_dir))
    dolog("removing <%s>" % out_abs_dir)
    shutil.rmtree(out_abs_dir)
    dolog("moving2: <%s> to <%s>" % (os.path.join(get_parent_path(out_abs_dir), 'OOPSevaluation'), out_abs_dir))
    shutil.move(os.path.join(get_parent_path(out_abs_dir), 'OOPSevaluation'), out_abs_dir)
    return ""


def parse_oops_issues(oops_rdf):
    p = rdfxml.parseRDF(oops_rdf)
    raw_oops_list = p.result
    oops_issues = {}

    # Filter #1
    # Construct combine all data of a single elements into one json like format
    for r in raw_oops_list:
        if r['domain'] not in oops_issues:
            oops_issues[r['domain']] = {}
        oops_issues[r['domain']][r['relation']] = r['range']

    # Filter #2
    # get rid of elements without issue id
    oops_issues_filter2 = {}
    for i in oops_issues:
        if '#' not in i:
            oops_issues_filter2[i] = oops_issues[i]

    # Filter #3
    # Only include actual issues (some data are useless to us)
    detailed_desc = []
    oops_issues_filter3 = {}
    for i in oops_issues_filter2:
        if '<http://www.oeg-upm.net/oops#hasNumberAffectedElements>' in oops_issues_filter2[i]:
            oops_issues_filter3[i] = oops_issues_filter2[i]

    # Filter #4
    # Only include data of interest about the issue
    oops_issues_filter4 = {}
    issue_interesting_data = [
        '<http://www.oeg-upm.net/oops#hasName>',
        '<http://www.oeg-upm.net/oops#hasCode>',
        '<http://www.oeg-upm.net/oops#hasDescription>',
        '<http://www.oeg-upm.net/oops#hasNumberAffectedElements>',
        '<http://www.oeg-upm.net/oops#hasImportanceLevel>',
        # '<http://www.oeg-upm.net/oops#hasAffectedElement>',
        '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>',
    ]
    for i in oops_issues_filter3:
        oops_issues_filter4[i] = {}
        for intda in issue_interesting_data:
            if intda in oops_issues_filter3[i]:
                oops_issues_filter4[i][intda] = oops_issues_filter3[i][intda]
    return oops_issues_filter4, issue_interesting_data


def create_oops_issue_in_github(target_repo, ont_file, oops_issues):
    dolog('will create an oops issue')
    try:
        g.get_repo(target_repo).create_issue('OOPS! Evaluation for ' + ont_file, oops_issues)
    except Exception as e:
        dolog('exception when creating issue: ' + str(e))


def close_old_oops_issues_in_github(target_repo, ont_file):
    dolog('will close old issues')
    for i in g.get_repo(target_repo).get_issues(state='open'):
        if i.title == ('OOPS! Evaluation for ' + ont_file):
            i.edit(state='closed')


def nicer_oops_output(issues):
    sugg_flag = '<http://www.oeg-upm.net/oops#suggestion>'
    pitf_flag = '<http://www.oeg-upm.net/oops#pitfall>'
    warn_flag = '<http://www.oeg-upm.net/oops#warning>'
    num_of_suggestions = issues.count(sugg_flag)
    num_of_pitfalls = issues.count(pitf_flag)
    num_of_warnings = issues.count(warn_flag)
    # s=" OOPS has encountered %d pitfalls and %d
    # warnings"%(num_of_pitfalls,num_of_warnings)
    s = " OOPS! has encountered %d pitfalls" % (num_of_pitfalls)
    if num_of_warnings > 0:
        s += ' and %d warnings' % (num_of_warnings)
    if num_of_pitfalls == num_of_suggestions == num_of_warnings == 0:
        return ""
    if num_of_suggestions > 0:
        s += "  and have %d suggestions" % (num_of_suggestions)
    s += "."
    nodes = issues.split("====================")
    suggs = []
    pitfs = []
    warns = []
    for node in nodes[:-1]:
        attrs = node.split("\n")
        if sugg_flag in node:
            for attr in attrs:
                if 'hasDescription' in attr:
                    suggs.append(attr.replace('hasDescription: ', ''))
                    break
        elif pitf_flag in node:
            for attr in attrs:
                if 'hasName' in attr:
                    pitfs.append(attr.replace('hasName: ', ''))
                    break
        elif warn_flag in node:
            for attr in attrs:
                if 'hasName' in attr:
                    warns.append(attr.replace('hasName: ', ''))
                    break
        else:
            dolog('in nicer_oops_output: strange node: ' + node)
    if len(pitfs) > 0:
        s += "The Pitfalls are the following:\n"
        for i in range(len(pitfs)):
            s += '%d. ' % (i + 1) + pitfs[i] + "\n"
    if len(warns) > 0:
        s += "The Warning are the following:\n"
        for i in range(len(warns)):
            s += "%d. " % (i + 1) + warns[i] + "\n"
    if len(suggs) > 0:
        s += "The Suggestions are the following:\n"
        for i in range(len(suggs)):
            s += "%d. " % (i + 1) + suggs[i] + "\n"
    return s

