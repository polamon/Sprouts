# -*- coding: utf-8 -*-

from datetime import datetime
from lxml import etree

company_list = ['Google', 'Facebook', 'Linkedin', 'Amazon', 'Microsoft']
work_type_list = ['全职', '实习']
experience_list = ['fresh grad应届毕业生', '在职跳槽']

tag_to_type = {}
for company in company_list:
    tag_to_type[company] = "company"
for work_type in work_type_list:
    tag_to_type[work_type] = "work_type"
for experience in experience_list:
    tag_to_type[experience] = "experience"

class Post:
    """
    Holder class for post basic info and tags.
    """
    def __init__(self):
        self.tid = None
        self.title = None
        self.url = None
        self.age = None
        self.company = None
        self.work_type = None
        self.experience = None

    def __str__(self):
        for item in self.__dict__.items():
            print(item)
        return ""

def get_age_from_time(time):
    """
    Get age of the post from time description.
    """
    try:
        age = 0
        if time.endswith('小时前') or time.endswith('分钟前'):
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
        for k, v in tag_to_type.items():
            if k in tag:
                if v == 'company':
                    post.company = k
                if v == 'work_type':
                    post.work_type = k
                if v == 'experience':
                    post.experience = k
    return post

if __name__ == '__main__':
    with open("test/thread.html") as f:
        content = f.read()
        post = Post()
        populate_from_thread_page(post, content)
        print(post)
