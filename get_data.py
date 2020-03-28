import pandas as pd
import requests 
import json 
import os
import praw
import time

step_size = 500 # max size for pushshift 
with open('./post_list.txt', 'r') as f: 
    links = f.readlines()
    links = [l.replace('\n','').strip() for l in links]
comments = []
for l in links:
    print(l)
    post_id = l.split('comments/')[1].split('/')[0]
    print(post_id)
    r = requests.get('https://api.pushshift.io/reddit/submission/comment_ids/{}'.format(post_id))
    comment_ids = json.loads(r.text)['data']
    start_idx = 0 
    while start_idx < len(comment_ids): 
        end_index = min(start_idx + step_size, len(comment_ids))
        request_ids = ','.join(comment_ids[start_idx:end_index])
        r = requests.get('https://api.pushshift.io/reddit/comment/search?ids={}'.format(request_ids))

        comment_results = json.loads(r.text)['data']
        print(len(comments))
        comments += comment_results
        #print(start_idx)


        if len(comment_results) != (end_index - start_idx):
            print('only {} comments returned'.format(len(comment_results)))
        start_idx += step_size

    with open('./data/comments.json', 'w') as f: 
        f.write(json.dumps(comments)) 

