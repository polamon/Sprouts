# -*- coding: utf-8 -*-

import sys
from absl import app, flags
import requests
import time

from post import *
import gsheet

FLAGS = flags.FLAGS
flags.DEFINE_integer('page_num', 0, 'Number of forum pages to retrieve.')
flags.DEFINE_integer('max_age', 0, 'Max age of the posts to keep.')
flags.DEFINE_string('company', None, 'Name of specified company.')
flags.DEFINE_string('work_type', None, 'Work type (fulltime / intern).')
flags.DEFINE_string('sheet_id', None, 'Target Google sheet id.')
flags.DEFINE_bool('output', False, 'Whether to output to terminal.')

def filter_fn(post):
    if FLAGS.company:
        if not post.company or post.company != FLAGS.company:
            return False
    if FLAGS.work_type:
        if not post.work_type or post.work_type != FLAGS.work_type:
            return False
    return True

def main(argv):
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '\
                 '(KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
    headers = {'User-Agent': user_agent}

    posts = []
    for i in range(FLAGS.page_num):
        url = "http://www.1point3acres.com/bbs/forum-145-%s.html" %(i + 1)
        r = requests.get(url, headers = headers)
        forum_content = r.text
        posts.extend(parse_forum_page(forum_content))
    posts = list(filter(lambda post: post.url.startswith("http"), posts))

    posts = list(filter(lambda post: post.age <= FLAGS.max_age, posts))
    posts = sorted(posts, key = lambda post: post.tid)

    for post in posts:
        r = requests.get(post.url, headers = headers)
        thread_content = r.text
        populate_from_thread_page(post, thread_content)

    posts = list(filter(lambda post: filter_fn(post), posts))

    if FLAGS.output:
        for post in posts:
            print(post, '\n')

    if FLAGS.sheet_id:
        gsheet.write(posts, FLAGS.sheet_id)

if __name__ == '__main__':
  app.run(main)
