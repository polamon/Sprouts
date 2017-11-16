# -*- coding: utf-8 -*-

from absl import app, flags
import requests

from post import *
import gsheet

FLAGS = flags.FLAGS
flags.DEFINE_integer('page_num', 0, 'Number of forum pages to retrieve.')
flags.DEFINE_integer('max_age', 0, 'Max age of the posts to keep.')
flags.DEFINE_string('sheet_id', None, 'Target Google sheet id.')
flags.DEFINE_bool('display_only', False,
                  'Display all command line arguments only.')
flags.DEFINE_integer('logging_level', 0, '')

def main(argv):
    if FLAGS.display_only:
        print(FLAGS.sheet_id)

    user_agent = ('Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36')
    headers = {'User-Agent': user_agent}

    # 1. Gather posts from latest forum pages.
    posts = []
    for i in range(FLAGS.page_num):
        url = "http://www.1point3acres.com/bbs/forum-145-%s.html" %(i + 1)
        r = requests.get(url, headers = headers)
        forum_content = r.text
        posts.extend(parse_forum_page(forum_content))

    # 3. Filter posts by parameters given; sort posts by time.
    posts = list(filter(lambda post: post.age <= FLAGS.max_age, posts))
    posts = sorted(posts, key = lambda post: post.tid)

    # 2. Populate tags from corresponding thread page to post.
    for post in posts:
        r = requests.get(post.url, headers = headers)
        thread_content = r.text
        populate_from_thread_page(post, thread_content)

    # 4. Ouput posts to Google Sheet or terminal.
    if FLAGS.sheet_id:
        gsheet.write_to_gsheet(posts, FLAGS.sheet_id)
    else:
        for post in posts:
            print(post, '\n')

if __name__ == '__main__':
  app.run(main)
