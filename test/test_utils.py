# -*- coding: utf-8 -*-

import unittest
from freezegun import freeze_time
from sprouts.utils import *

class TestGetAgeFromTime(unittest.TestCase):
    def test_today(self):
        self.assertEqual(0, get_age_from_time('6 小时前'))

    def test_yesterday(self):
        self.assertEqual(1, get_age_from_time('昨天 04:05'))

    def test_the_day_before_yesterday(self):
        self.assertEqual(2, get_age_from_time('前天 13:01'))

    def test_k_days_age(self):
        self.assertEqual(6, get_age_from_time('6 天前'))

    @freeze_time('2017-11-11')
    def test_general_date(self):
        self.assertEqual(27, get_age_from_time('2017-10-15'))
