# -*- coding: utf-8 -*-

from absl import app, flags
import csv
from pyshorteners import Shortener
import requests
import time
from tqdm import *

from post import Post
import bbs_parser
import gsheet

FLAGS = flags.FLAGS

# post-gather settings
flags.DEFINE_integer('page_number', 0, 'Number of forum pages to retrieve.')
flags.DEFINE_integer('max_age', 0, 'Max age of the posts to keep.')

# filter settings
flags.DEFINE_bool('keep_missing_tag', False,
                  'Keep posts with missing tag when applying filters.')
flags.DEFINE_string('company', None,
                    'Keep posts of specified company.')
flags.DEFINE_string('work_type', None,
                    'Keep posts of specified work type.'
                    '(Fulltime / Intern)')
flags.DEFINE_string('experience', None,
                    'Keep posts of specified experience requirement.'
                    '(New Grad / Experienced)')

# output settings
flags.DEFINE_string('gsheet_id', None, 'Target Google Sheet id.')
flags.DEFINE_string('csv_file', None, 'Target csv file name.')

# misc settings
flags.DEFINE_bool('display_only', False,
                  'If true, only display all command line arguments.')
flags.DEFINE_bool('use_shortened_url', False,
                  'If true, use Tinyurl to shorten url in output.')
flags.DEFINE_bool('print_all_posts', False,
                  'If true, print all posts when running (for debug use).')

def sanity_check():
    if not FLAGS.gsheet_id and not FLAGS.csv_file:
        print('No ouput destination specified. '
              'Please provide --gsheet_id or --csv_file.')
        return False
    return True

def filter_fn(post):
    # filter by company
    if FLAGS.company:
        if not post.company:
            if not FLAGS.keep_missing_tag:
                return False
        elif post.company != FLAGS.company:
                return False
    # filter by work type
    if FLAGS.work_type:
        if not post.work_type:
            if not FLAGS.keep_missing_tag:
                return False
        elif post.work_type != FLAGS.work_type:
                return False
    # filter by experience
    if FLAGS.experience:
        if not post.experience:
            if not FLAGS.keep_missing_tag:
                return False
        elif post.experience != FLAGS.experience:
                return False
    return True

def main(argv):
    if FLAGS.display_only:
        print('page_number: %d' %(FLAGS.page_number))
        print('max_age: %d' %(FLAGS.max_age))
        print('gsheet_id: %s' %(FLAGS.gsheet_id))
        return

    if not sanity_check():
        return

    user_agent = ('Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36')
    headers = {'User-Agent': user_agent}

    # Gather posts from latest forum pages.
    posts = []
    for i in range(FLAGS.page_number):
        url = "http://www.1point3acres.com/bbs/forum-145-%s.html" %(i + 1)
        r = requests.get(url, headers = headers)
        forum_content = r.text
        posts.extend(bbs_parser.parse_forum_page(forum_content))

    # Filter posts by age; sort posts by time.
    posts = list(filter(lambda post: post.age <= FLAGS.max_age, posts))
    posts = sorted(posts, key = lambda post: post.tid)

    # Populate tags from corresponding thread page to post.
    for post in tqdm(posts, desc = 'Retrieving posts...'):
        r = requests.get(post.url, headers = headers)
        thread_content = r.text
        bbs_parser.populate_from_thread_page(post, thread_content)
        if FLAGS.print_all_posts:
            print(post, '\n')

        # (Don't) Be Evil
        time.sleep(0.5)

    # Further filter posts.
    posts = list(filter(filter_fn, posts))

    if FLAGS.use_shortened_url:
        for post in posts:
            shortener = Shortener('Tinyurl')
            post.url = shortener.short(post.url)

    # Ouput posts to Google Sheet or local csv file.
    schema = Post.schema()
    values = [post.tolist() for post in posts]

    if FLAGS.gsheet_id:
        gsheet.write_to_gsheet(FLAGS.gsheet_id, schema, values)
        print('Successfully written to Google Sheet %s' %(FLAGS.gsheet_id))

    if FLAGS.csv_file:
        with open(FLAGS.csv_file, 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(schema)
            f_csv.writerows(values)
            print('Successfully written to file %s' %(FLAGS.csv_file))

if __name__ == '__main__':
  app.run(main)
