# -*- coding: utf-8 -*-

import sys
from absl import app, flags
import requests
import time

from post import *

FLAGS = flags.FLAGS
flags.DEFINE_integer('forum_page_num', 0, 'Number of forum pages to retrieve.')
flags.DEFINE_integer('max_post_age', 0, 'Max age of the posts to keep.')
flags.DEFINE_string('sheet_id', None, 'Target Google sheet id.')

def main(argv):
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '\
                 '(KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
    headers = {'User-Agent': user_agent}

    posts = []
    for i in range(FLAGS.forum_page_num):
        url = "http://www.1point3acres.com/bbs/forum-145-%s.html" %(i + 1)
        r = requests.get(url, headers = headers)
        forum_content = r.text
        posts.extend(parse_forum_page(forum_content))

    posts = list(filter(lambda post: post.url.startswith('http'), posts))
    posts = list(filter(lambda post: post.age <= FLAGS.max_post_age, posts))
    posts = sorted(posts, key = lambda post: post.tid)

    for post in posts:
        r = requests.get(post.url, headers = headers)
        thread_content = r.text
        populate_from_thread_page(post, thread_content)
        print(post)

if __name__ == '__main__':
  app.run(main)
