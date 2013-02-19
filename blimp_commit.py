import os
import json
import re

import blimp
from flask import Flask, request

app = Flask(__name__)

api_username = ""
api_key = ""
app_id = ""
app_secret = ""
blimp_userid = ""


def get_env_setting(setting):
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise RuntimeError(error_msg)

API_USERNAME = get_env_setting('BLIMP_USERNAME')
API_KEY = get_env_setting('BLIMP_API_KEY'),
APP_ID = get_env_setting('BLIMP_APP_ID'),
APP_SECRET = get_env_setting('BLIMP_APP_SECRET')


def update_task(task_id, commit_msg, url, author):
    api = blimp.Client(API_USERNAME, API_KEY, APP_ID, APP_SECRET)
    comment = "%s: %s\n%s" % (
        author, 
        commit_msg.replace('t%s' % task_id, '').replace('#done', ''),
        url)
    comment_obj = {
        'comment': comment,
        'object_pk': task_id,
        'user': u'/api/v2/user/%s/' % blimp_userid,
        'content_type': u'todo',
    }
    comment_req = api.comment.create(comment_obj)
    if '#done' in commit_msg:
        task = api.task.get(task_id)
        task_req = api.task.update(task['id'], {"state": "done"})


@app.route("/hook/github", methods=['POST'])
def gh_hook():
    if request.method == 'POST':
        data = json.loads(request.data)
        if 'commits' in data:
            for commit in data['commits']:
                message = commit['message']
                match = re.search(r't(\d+)\s*', message)
                if match:
                    task_id = match.group(1)
                    update_task(
                        task_id,
                        message,
                        commit['url'],
                        commit['author']['name']
                    )

    return "Okay"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8002)
