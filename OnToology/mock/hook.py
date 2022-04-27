

def get_webhook(url, hook_id=12345678):
    j = {
      "type": "Repository",
      "id": hook_id,
      "name": "web",
      "active": true,
      "events": [
        "push",
        "pull_request"
      ],
      "config": {
        "content_type": "json",
        "insecure_ssl": "0",
        "url": url
      },
      "updated_at": "2019-06-03T00:57:16Z",
      "created_at": "2019-06-03T00:57:16Z",
      "url": "https://api.github.com/repos/octocat/Hello-World/hooks/12345678",
      "test_url": "https://api.github.com/repos/octocat/Hello-World/hooks/12345678/test",
      "ping_url": "https://api.github.com/repos/octocat/Hello-World/hooks/12345678/pings",
      "deliveries_url": "https://api.github.com/repos/octocat/Hello-World/hooks/12345678/deliveries",
      "last_response": {
        "code": null,
        "status": "unused",
        "message": null
      }
    }
    return j


def get_webhooks(url, hook_id=12345678):
    j = [
        {
            "type": "Repository",
            "id": hook_id,
            "name": "web",
            "active": true,
            "events": [
                "push",
                "pull_request"
            ],
            "config": {
                "content_type": "json",
                "insecure_ssl": "0",
                "url": url
            },
            "updated_at": "2019-06-03T00:57:16Z",
            "created_at": "2019-06-03T00:57:16Z",
            "url": "https://api.github.com/repos/octocat/Hello-World/hooks/12345678",
            "test_url": "https://api.github.com/repos/octocat/Hello-World/hooks/12345678/test",
            "ping_url": "https://api.github.com/repos/octocat/Hello-World/hooks/12345678/pings",
            "deliveries_url": "https://api.github.com/repos/octocat/Hello-World/hooks/12345678/deliveries",
            "last_response": {
                "code": null,
                "status": "unused",
                "message": null
            }
        }
    ]
    return j
