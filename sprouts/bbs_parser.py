# -*- coding: utf-8 -*-

from lxml import etree
from post import Post
from utils import get_age_from_time

"""
Raw tags in thread pages.
"""
company_list = ['Airbnb', 'Amazon', 'Apple', 'Bloomberg', 'Cisco', 'Dropbox',
                'eBay', 'EMC', 'Facebook', 'Google', 'Intel', 'Linkedin',
                'Microsoft', 'Nvidia', 'Oracle', 'Snapchat', 'Twitter',
                'TwoSigma', 'Uber', 'VMWare', 'Yahoo', 'Yelp']

work_type_list = [('全职', 'fulltime'), ('实习', 'intern')]

experience_list = [('fresh grad', 'new grad'),
                   ('在职跳槽', 'experienced')]


def parse_forum_page(forum_content):
    """
    Parse forum page to get a list of Post objects.
    A forum page is like: http://www.1point3acres.com/bbs/forum-145-1.html
    """
    selector = etree.HTML(forum_content)
    thread_elmts = selector.xpath('//*/tr/th/a[2]')
    time_elmts = selector.xpath('//*/tr/td[2]/em/span')

    posts = []
    for thread_elmt, time_elmt in zip(thread_elmts, time_elmts):
        post = Post()
        post['title'] = thread_elmt.text
        post['url'] = thread_elmt.get('href')
        if not post['url'].startswith('http'):
            continue

        for x in post['url'].split('&'):
            if x.startswith('tid='):
                post['tid'] = eval(x[4:])
                break

        time = time_elmt.text
        if not time:
            time = [e.text for e in time_elmt if e.text][0]
        post['age'] = get_age_from_time(time)

        posts.append(post)
    return posts


def populate_from_thread_page(post, thread_content):
    """
    Parse thread page to populate fields in Post object.
    A thread page is like: http://www.1point3acres.com/bbs/forum.php?mod=viewthread&tid=301284
    """
    selector = etree.HTML(thread_content)
    tag_elmts = selector.xpath('//*/tr[1]/td[2]/div[2]/div/span/node()')

    tags = []
    for tag_elmt in tag_elmts:
        if isinstance(tag_elmt, etree._ElementUnicodeResult):
            tags.append(str(tag_elmt))
        else:
            tags.extend([e.text for e in list(tag_elmt.iter()) if e.text])
    tags_text = " ".join(tags)

    for company in company_list:
        if company in tags_text:
            post['company'] = company
    for work_type in work_type_list:
        if work_type[0] in tags_text:
            post['work_type'] = work_type[1]
    for experience in experience_list:
        if experience[0] in tags_text:
            post['experience'] = experience[1]
