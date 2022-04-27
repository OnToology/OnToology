from OnToology.autoncore import remove_webhook
from OnToology.models import OUser, Repo
import traceback


def delete_repo_action(repo=None, repo_id=None, user=None, host=""):
    if repo:
        rs = user.repos.filter(url=repo)
    elif repo_id:
        rs = user.repos.filter(id=repo_id)
    else:
        raise Exception("repo or repo_id should be passed")
    try:
        if len(rs) < 1:
            return {'status': False, 'error': 'Invalid Repo', 'status_code': 404}
        r = rs[0]
        repo_url = r.url
        r.delete()
        remove_webhook(repo_url, host + "/add_hook")
        return {'status': True, 'status_code': 204}
    except Exception as e:
        print("error deleting the webhook: " + str(e))
        traceback.print_exc()
        return {'status': False, 'error': str(e), 'status_code': 500}
