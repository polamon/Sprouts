# -*- coding: utf-8 -*-

import unittest

from sprouts.post import *

class TestPost(unittest.TestCase):
    def test_schema(self):
        expected_schema = ['tid', 'Title', 'Age(day)', 'Company', 'Work Type',
                           'Experience', 'url']
        self.assertCountEqual(Post.schema(), expected_schema)

    def test_to_list(self):
        post = Post()
