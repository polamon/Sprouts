# -*- coding: utf-8 -*-

from absl import app, flags
import requests
import multiprocessing
from tqdm import *
import csv
from pyshorteners import Shortener

from post import Post
import bbs_parser
import gsheet

"""
command line flags
"""
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
flags.DEFINE_bool('use_shortened_url', False,
                  'If true, use Tinyurl to shorten url in output.')
flags.DEFINE_bool('print_all_posts', False,
                  'If true, print all posts when running (for debug use).')

"""
request headers
"""
user_agent = ('Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36')
headers = {'User-Agent': user_agent}


def sanity_check():
    """
    guarantees there will be some output
    """
    if FLAGS.print_all_posts:
        return True
    if not FLAGS.gsheet_id and not FLAGS.csv_file:
        print('No ouput destination specified. '
              'Please provide --gsheet_id or --csv_file.')
        return False
    return True


def build_filter(attribute, target):
    def f(post):
        if not post[attribute]:
            return FLAGS.keep_missing_tag
        else:
            return post[attribute] == target
    return f


def filter_fn(post):
    attribute_filters = []
    if FLAGS.company:
        attribute_filters.append(build_filter('company', FLAGS.company))
    if FLAGS.work_type:
        attribute_filters.append(build_filter('work_type', FLAGS.work_type))
    if FLAGS.experience:
        attribute_filters.append(build_filter('experience', FLAGS.experience))
    return all([f(post) for f in attribute_filters])


def handle_post(post):
    r = requests.get(post['url'], headers=headers)
    bbs_parser.populate_from_thread_page(post, r.text)
    return post


def main(argv):
    if not sanity_check():
        return

    # Gather posts from latest forum pages.
    posts = []
    for i in range(FLAGS.page_number):
        url = "http://www.1point3acres.com/bbs/forum-145-%s.html" % (i + 1)
        r = requests.get(url, headers=headers)
        posts.extend(bbs_parser.parse_forum_page(r.text))

    # Filter posts by age.
    posts = list(filter(lambda post: post['age'] <= FLAGS.max_age, posts))

    # Populate tags from corresponding thread page to post.
    pool = multiprocessing.Pool(processes=4)
    posts = [post for post in tqdm(pool.imap_unordered(handle_post, posts),
                                   total=len(posts),
                                   desc='Retrieving posts...')]

    if FLAGS.print_all_posts:
        for post in posts:
            print(post, '\n')

    # Further filter posts. Sort posts by tid.
    posts = list(filter(filter_fn, posts))
    posts = sorted(posts, key=lambda post: post['tid'])

    if FLAGS.use_shortened_url:
        for post in posts:
            shortener = Shortener('Tinyurl')
            post.url = shortener.short(post.url)

    # Ouput posts to Google Sheet or local csv file.
    schema = Post.display_names
    values = [post.to_list() for post in posts]

    if FLAGS.gsheet_id:
        gsheet.write_to_gsheet(FLAGS.gsheet_id, schema, values)
        print('Successfully written to Google Sheet %s' % (FLAGS.gsheet_id))

    if FLAGS.csv_file:
        with open(FLAGS.csv_file, 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(schema)
            f_csv.writerows(values)
            print('Successfully written to file %s' % (FLAGS.csv_file))


if __name__ == '__main__':
    app.run(main)
