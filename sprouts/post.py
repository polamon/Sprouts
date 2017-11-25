# -*- coding: utf-8 -*-


class Post(dict):
    """
    holder class for post summary
    """

    # attributes in post summary
    attributes = ['tid', 'title', 'age', 'company', 'work_type',
                  'experience', 'text', 'url']

    # display name for attributes, used when saving to file
    display_names = ['tid', 'Title', 'Age', 'Company', 'Work Type',
                     'Experience', 'Text', 'url']

    def __init__(self):
        for attr in Post.attributes:
            self[attr] = None

    def __getitem__(self, k):
        if k not in Post.attributes:
            raise KeyError('')
        return super().__getitem__(k)

    def __setitem__(self, k, v):
        if k not in Post.attributes:
            raise KeyError('')
        super().__setitem__(k, v)

    def __str__(self):
        l = []
        for (attr, name) in zip(Post.attributes, Post.display_names):
            l.append('%s = %s' % (name, self[attr]))
        return '\n'.join(l)

    def to_list(self, schema = None):
        return [self[attr] for attr in Post.attributes]
