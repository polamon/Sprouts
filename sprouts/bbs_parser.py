# -*- coding: utf-8 -*-

from datetime import datetime
from lxml import etree

from post import Post

company_list = ['Airbnb', 'Amazon', 'Apple', 'Bloomberg', 'Cisco', 'Dropbox',
                'eBay', 'EMC', 'Facebook', 'Google', 'Intel', 'Linkedin',
                'Microsoft', 'Nvidia', 'Oracle', 'Snapchat', 'Twitter',
                'TwoSigma', 'Uber', 'VMWare', 'Yahoo', 'Yelp']

work_type_list = ['全职', '实习']

experience_list = ['fresh grad应届毕业生', '在职跳槽']

TAGS = {}
for company in company_list:
    TAGS[company] = "company"
for work_type in work_type_list:
    TAGS[work_type] = "work_type"
for experience in experience_list:
    TAGS[experience] = "experience"

def get_age_from_time(time):
    """
    Get age of the post from time description.
    """
    try:
        age = 0
        if time.endswith(('秒前', '小时前', '分钟前')):
            age = 0
        elif time.startswith('昨天'):
            age = 1
        elif time.startswith('前天'):
            age = 2
        elif time.endswith('天前'):
            age = eval(time[:-2].strip())
        else:
            l = [int(x) for x in time.split('-')]
            if len(l) != 3:
                raise ValueError('invalid time expression: %s' %(time))
            post_day = datetime(*l)
            age = (datetime.today() - post_day).days
        return age
    except:
        print('invalid time expression: %s' %(time))
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
        post.title = thread_elmt.text
        post.url = thread_elmt.get('href')
        if not post.url.startswith('http'):
            continue

        for x in post.url.split('&'):
            if x.startswith('tid='):
                post.tid = eval(x[4:])

        time = time_elmt.text
        if not time:
            time = [e.text for e in time_elmt if e.text][0]
        post.age = get_age_from_time(time)

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

    for tag in tags:
        for k, v in TAGS.items():
            if k in tag:
                if v == 'company':
                    post.company = k
                if v == 'work_type':
                    if k == '全职':
                        post.work_type = 'Fulltime'
                    else:
                        post.work_type = 'Intern'
                if v == 'experience':
                    if k == 'fresh grad应届毕业生':
                        post.experience = 'Fresh Grad'
                    else:
                        post.experience = 'Experienced'
