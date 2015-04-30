#! /usr/bin/env python
import numpy as np
import os
import matplotlib.pyplot as plt
from collections import namedtuple
from operator import itemgetter

str_path = 'tracker_demo/str/_images/'

# collections of named tuple
score_statistic = namedtuple('score', 'path videonum mean std max min')
# a Tracker dict
T = {}
attr_set = []
results = []
total_scores = []

def plot_hist(x, bin_num):
    hist, bins = np.histogram(x, bin_num)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()

# traverse all score values
for root, dirs, files in os.walk(str_path):
    for f in files:
        if f.endswith('txt'):
            type_ = f.split('-')[1].rstrip('.txt').split('_')
            attr = type_[0]
            attr_set.append(attr)
            video_num = type_[1]
            score_path = '/'.join([root, f])
            score = np.genfromtxt(score_path, dtype=[('index', int), ('score', float)], delimiter=',')
            avg_ = np.mean(score['score'])
            std_ = np.std(score['score'])
            max_= np.max(score['score'])
            min_= np.min(score['score'])
            total_scores.extend(score['score'])
            # set the dict which key=attribute, value is a tuple list
            T.setdefault(attr, []).append(score_statistic(score_path, video_num, avg_, std_, max_, min_))

attr_set = set(attr_set)
# travel through all attribute
output_format = '%16s\t%15s\t%15s\t%15s\t%15s\t%15s\t%15s\t%15s\t%15s'
line = output_format % ('Attribute' ,'Mean score', 'Std', 'Max score', 'Min score', 'best mean', 'min std', 'worst mean', 'max std')
print line
for attr_ in attr_set:
    cur_list = T[attr_]
    mean_list = []
    max_list = []
    std_list = []
    min_list = []
    for i, s in enumerate(cur_list):
        mean_list.append(s.mean)
        max_list.append(s.max)
        min_list.append(s.min)
        std_list.append(s.std)
    Mean_ = np.mean(mean_list)
    Max_ = np.max(max_list)
    Min_ = np.min(min_list)
    score_ = np.genfromtxt(s.path, dtype=[('index', int), ('score', float)], delimiter=',')
    Std_ = np.std(score_['score'])
    # show statics in each attributes
    best_avg = max(cur_list,key=itemgetter(1))[1]
    worst_avg = min(cur_list,key=itemgetter(1))[1]
    min_std = min(cur_list, key=itemgetter(2))[1]
    max_std = max(cur_list, key=itemgetter(2))[1]
    line = output_format % (attr_, str(Mean_), str(Std_), str(Max_), str(Min_), best_avg, min_std, worst_avg, max_std)
    print line
total_mean = np.mean(total_scores)
total_std = np.std(total_scores)
print 'Overall Behavior of the tracker ==> mean: %12s\tstd: %12s\t' % (str(total_mean), str(total_std))


# -- orginal data
bin_num = 100
x = total_scores
#plot_hist(x, bin_num)

# -- threhold 0.8
x_np = np.asarray(x)
low_value_indices = x_np < .8
x_np[low_value_indices] = 0
x_thres = np.sort(x_np[x_np >= .8])
plot_hist(x_thres , 100)
