# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread
import jieba.analyse
from wordcloud import WordCloud, ImageColorGenerator

# concatenate all post text together
all_text = None
with open('data.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    text = [row[-2] for row in reader]
    all_text = '\n'.join(text)

# get keywords list
jieba.analyse.set_stop_words('stop_words.txt')
keywords = jieba.analyse.extract_tags(all_text, topK=300, withWeight=False)

# read mask image
mask = np.array(imread("mask.png"))

# generate word cloud
wc = WordCloud(background_color='white',
               font_path='Microsoft Yahei.ttf',
               mask=mask,
               max_words=300,
               max_font_size=60,
               random_state=42)
wc.generate(' '.join(keywords))
wc.recolor(color_func=ImageColorGenerator(mask))

plt.imshow(wc)
plt.axis("off")
plt.show()
wc.to_file('word_cloud.png')
