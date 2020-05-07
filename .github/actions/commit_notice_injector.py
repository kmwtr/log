#! python3
import os
import logging as log
from twitter import Twitter, OAuth
import json

# Debug
# -------------------------------------------------
log.basicConfig(level=log.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')


# -------------------------------------------------
json_load = json.loads(os.getenv('GITHUB_CONTEXT'))

commit_id = str(json_load['event']['head_commit']['id'])[0:4]
message =   str(json_load['event']['head_commit']['message']).splitlines()
phrase =    str(os.getenv('msg_A'))

files_str = os.getenv('ADDED_FILES')
files = files_str.strip('[]')
files = files.split(',')

msg = '[ Log was updated ]' + ' ID: ' + commit_id + ' | File: ' + str(files[0]) + ' | Summary: ' + str(message[0]) + ' | ' + phrase


# Twitter API
# -------------------------------------------------
my_auth = OAuth(
    os.getenv('TWITTER_ACCESS_TOKEN'), 
    os.getenv('TWITTER_ACCESS_TOKEN_SECRET'), 
    os.getenv('TWITTER_API_KEY'),
    os.getenv('TWITTER_API_SECRET_KEY')
    )


# 
# -------------------------------------------------
def commit_notice_injector():
    t = Twitter(auth=my_auth)
    
    with open(str(files[0]), "rb") as imagefile:
        imagedata = imagefile.read()

    t_upload = Twitter(domain="upload.twitter.com", auth=my_auth)
    id_img = t_upload.media.upload(media=imagedata)["media_id_string"]
    
    t.statuses.update(status=msg, media_ids=id_img)


# 
# - - - - - - - - - - - - - - - - - - - - -
commit_notice_injector()
