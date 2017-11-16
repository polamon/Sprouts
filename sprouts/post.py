# -*- coding: utf-8 -*-

class Post:
    """
    Holder class for post summary.
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
        return "\n".join(["%s : %s" % (str(k), str(v)) for (k, v) in
                            self.__dict__.items()])

    @staticmethod
    def schema():
        return ['tid', 'Title', 'Age(day)', 'Company', 'Work Type',
                'Experience', 'Url']

    def tolist(self):
        return [self.tid, self.title, self.age, self.company, self.work_type,
                self.experience, self.url]
