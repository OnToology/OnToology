
import os
from github import Github
import os
import sys

ontology_formats = ['.rdf', '.owl', '.ttl']


def get_ontologies(file_or_dir, repo):
    """
    :param file_or_dir: FileContent
    :param repo: Repository
    :return: list of ontologies
    """
    if file_or_dir.type == 'file':
        ext = file_or_dir.name[-4:]
        if ext in ontology_formats:
            return [file_or_dir]
        else:
            return []

    elif file_or_dir.type == 'dir':
        path = file_or_dir.path
        #print 'path: %s' % path
        files_or_dirs = repo.get_file_contents(path)
        ontologies = []
        for fd in files_or_dirs:
            ontos = get_ontologies(fd, repo)
            ontologies += ontos
        return ontologies
    else:
        print 'type error: <%s>' % str(file_or_dir.type)
        return []


def ontologies_for_repo(repo):
    """
    :param repo: repo string as "user/reponame"
    :return: ontologies list
    """
    g = Github(os.environ['github_username'], os.environ['github_password'])
    try:
        repo = g.get_repo(repo)
        files_and_dirs = repo.get_file_contents('/')
        files_and_dirs = [fd for fd in files_and_dirs if fd.name != 'OnToology']
        # for fd in files_and_dirs:
        #     print fd.name + ' => ' + fd.type
        ontologies = []
        for fd in files_and_dirs:
            ontos = get_ontologies(fd, repo)
            ontologies += ontos
        return ontologies
    except Exception as e:
        print str(e)
        return []


def ontologies_for_repos(repos):
    html = ""
    for i, repo in enumerate(repos):
            print "handling repo (%d): %s" % (i, repo)
            ontos = ontologies_for_repo(repo)
            for o in ontos:
                html += "<tr><td>%s</td><td>%s</td></tr>\n" % (repo, o.path)
    print html


def main(file_dir):
    ignore_words = ['test', 'demo', 'ahmad88me']
    print "opening file: "+file_dir
    f = open(file_dir)
    repos = list(set([line.strip() for line in f.readlines()]))
    clean_repos = []
    print "number of repos: "+str(len(repos))
    for repo in repos:
        ignore_repo = False
        print "repo: "+repo
        for iw in ignore_words:
            if iw in repo.lower():
                ignore_repo = True
                break
        if ignore_repo:
            print 'ignore repo: ' + repo
        else:
            clean_repos.append(repo)
    ontologies_for_repos(clean_repos)


if __name__ == "__main__":
    main(sys.argv[1])

