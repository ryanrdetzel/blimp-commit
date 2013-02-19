Set the follow environmental variables

API_USERNAME = get_env_setting('BLIMP_USERNAME')
API_KEY = get_env_setting('BLIMP_API_KEY'),
APP_ID = get_env_setting('BLIMP_APP_ID'),
APP_SECRET = get_env_setting('BLIMP_APP_SECRET')

Run this somewhere and point your github/bitbucket hook settings to the url. If you comment on a commit message with tNUM where tNUM is the task id then a comment will be posted to that blimp ticket with the commit message, the author and a link to the commit.
