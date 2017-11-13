# -*- coding: utf-8 -*-

import requests
import time

from post import *

user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '\
             '(KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
headers = {'User-Agent': user_agent}

posts = []
for i in range(1, 3):
    url = "http://www.1point3acres.com/bbs/forum-145-%s.html" %(i)
    r = requests.get(url, headers = headers)
    posts.extend(parse_forum_page(r.text))

posts = list(filter(lambda post: post.url.startswith('http'), posts))
posts = sorted(posts, key = lambda post: post.age)

for post in posts[:3]:
    r = requests.get(post.url, headers = headers)
    populate_from_thread_page(post, r.text)
    print(post)
