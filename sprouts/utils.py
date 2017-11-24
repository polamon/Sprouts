# -*- coding: utf-8 -*-

from datetime import datetime

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
                raise ValueError('invalid time expression: %s' %(time))
            post_day = datetime(*l)
            return (datetime.today() - post_day).days
    except:
        print('invalid time expression: %s' %(time))
        raise
