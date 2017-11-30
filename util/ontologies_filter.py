
import os
from github import Github


def ontologies_for_repo(repo):
    """
    :param repo: repo string as "user/reponame"
    :return: ontologies list
    """
    g = Github(os.environ['github_username'], os.environ['github_password'])
    repo = g.get_repo(repo)
    sha = repo.get_file_contents('/').sha
