# -*- coding: utf-8 -*-

import unittest
from sprouts.post import *


class TestPost(unittest.TestCase):
    def test_display_names(self):
        expected_display_names = ['tid', 'Title', 'Age', 'Company',
                                  'Work Type', 'Experience', 'Text', 'url']
        self.assertEqual(Post.display_names, expected_display_names)

    def test_set_and_get(self):
        p = Post()
        # attribute
        p['tid'] = 123
        self.assertEqual(p['tid'], 123)
        # non-attribute
        self.assertRaises(KeyError, lambda: p.__getitem__('ttid'))
        self.assertRaises(KeyError, lambda: p.__setitem__('ttid', 456))

    def test_str(self):
        p = Post()
        p['tid'] = 123
        p['title'] = 'Hello'

        expected_string = (
            "tid = 123\n"
            "Title = Hello\n"
            "Age = None\n"
            "Company = None\n"
            "Work Type = None\n"
            "Experience = None\n"
            "Text = None\n"
            "url = None")
        self.assertEqual(str(p), expected_string)

    def test_to_list(self):
        p = Post()
        p['tid'] = 123
        p['title'] = 'Hello'
        p['experience'] = 'Experienced'

        expected_list = [123, 'Hello', None, None, None, 'Experienced',
                         None, None]
        self.assertEqual(p.to_list(), expected_list)
