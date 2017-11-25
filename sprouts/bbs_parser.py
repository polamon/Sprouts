# -*- coding: utf-8 -*-

from datetime import datetime
from lxml import etree
from post import Post

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


def get_age_from_time(time):
    """
    Get age of the post from time description.
    """
    try:
        if time.endswith(('秒前', '小时前', '分钟前')):
            return 0
        elif time.startswith('昨天'):
            return 1
        elif time.startswith('前天'):
            return 2
        elif time.endswith('天前'):
            return eval(time[:-2].strip())
        else:
            l = [int(x) for x in time.split('-')]
            if len(l) != 3:
                raise ValueError('invalid time expression: %s' % (time))
            post_day = datetime(*l)
            return (datetime.today() - post_day).days
    except:
        print('invalid time expression: %s' % (time))
        raise


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


def populate_tags(post, thread_content):
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


def populate_text(post, thread_content):
    rubbish = ['attach_nopermission attach_tips',
               'locked', 'quote', 'guestviewthumb_cur']

    selector = etree.HTML(thread_content)
    text_segments = []
    for elmt in selector.xpath('//*[contains(@id, "message")]/node()'):
        if isinstance(elmt, etree._ElementUnicodeResult):
            text_segments.append(elmt.strip())
        else:
            attrib = elmt.attrib
            if 'class' in attrib:
                if attrib['class'] in rubbish:
                    continue
            for sub_elmt in list(elmt.iter()):
                if not sub_elmt.text:
                    continue
                if sub_elmt.tag == 'font':
                    continue
                attrib = sub_elmt.attrib
                if 'class' in attrib and attrib['class'] in rubbish:
                    continue
                text_segments.append(sub_elmt.text.strip())

    post['text'] = '\n'.join(filter(lambda s: len(s) > 0, text_segments))
