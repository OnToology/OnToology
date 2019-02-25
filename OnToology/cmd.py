import os
import sys
#################################################################
#           TO make this app compatible with Django             #
#################################################################

proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
print("proj_path: "+proj_path)
venv_python = os.path.join(proj_path, '.venv', 'bin', 'python')
# # This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnToology.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


def get_stats():
    stats = {
        'mean': 0,
        'median': 0,
        'num_of_ontologies': 0,
        'num_of_repos': 0,
        'num_of_pub': 0,
        'num_of_reg_users': 0,
    }
    repos = Repo.objects.all()
    ontologies_per_repo = []
    num_corr_repos = 0  # number of repos that has at least one ontology
    for r in repos:
        ontos = get_ontologies_in_online_repo(r.url)
        if ontos != []:
            ontologies_per_repo.append(len(ontos))
            num_corr_repos += 1
    num_of_ontologies = sum(ontologies_per_repo)
    stats['mean'] = num_of_ontologies/num_corr_repos
    if num_corr_repos > 0:
        ontologies_per_repo = sorted(ontologies_per_repo)
        if num_corr_repos % 2 == 0:  # even
            idx = (num_corr_repos-1)/2
            stats['median'] = (ontologies_per_repo[idx] + ontologies_per_repo[idx+1]) / 2
        else:
            idx = num_corr_repos/2
            stats['median'] = ontologies_per_repo[idx]
    stats['num_of_ontologies'] = num_of_ontologies
    stats['num_of_repos'] = len(repos)
    stats['num_of_pub'] = len(PublishName.objects.all())
    stats['num_of_reg_users'] = len(OUser.objects.all())
    return stats


def update_stats():
    stats = get_stats()
    stats_html = """
{% extends "base.html"%}
{%block body%}
    The average number of ontologies per repository: %d</br>
    The median number of ontologies per repository: %d</br>
    The total number of ontologies: %d</br>
    The total number of repositories: %d</br>
    The total number of published ontologies: %d</br>
    The total number of registered users: %d</br>
{% endblock %}
    """ % (
        stats['mean'],
        stats['median'],
        stats['num_of_ontologies'],
        stats['num_of_repos'],
        stats['num_of_pub'],
        stats['num_of_reg_users']
    )
    stats_dir = os.path.join(settings.BASE_DIR, 'templates', 'stats.html')
    f = open(stats_dir)
    f.write(stats_html)
    f.close()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'updatestats':
            update_stats()

