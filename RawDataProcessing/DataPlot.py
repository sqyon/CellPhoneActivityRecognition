import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import random
import GetFeature
import math
import os

def creatsampel():
	av, ah = [], []
	label = []
	with open('rawdata.csv') as f:
		reader = csv.reader(f)
		next(reader)
		for row in reader:
			av.append(float(row[1]))
			ah.append(float(row[2]))
			label.append(((row[3])))
	feed = [[]]
	avser, ahser, feature, lab = [], [], [], []
	steplen = 100

	id = {'downstairs': 0, 'jog': 1, 'sit': 2, 'stand': 3, 'upstairs': 4, 'walk': 5}
	cnt = [0, 0, 0, 0, 0, 0]

	for i in range(0, len(av) - steplen):
		if (i % 50 == 0):
			print('feature ', i, '/', len(av))
		else:
			continue
		flag = False
		for j in range(0, steplen):
			if label[i + j] != label[i] or cnt[id[label[i]]] > 1000:
				flag = True
		if flag:
			continue
		tav, tah = [], []
		for j in range(0, steplen):
			tav.append(av[i + j])
			tah.append(ah[i + j])
		tav = GetFeature.running_mean(tav)
		tah = GetFeature.running_mean(tah)
		avser.append(str(tav))
		ahser.append(str(tah))
		# feature.append(str(fea))
		lab.append(label[i])
		cnt[id[label[i]]] = cnt[id[label[i]]] + 1
	if len(feed[0]) == 0:
		feed.pop(0)
	df = {'av': avser, 'ah': ahser, 'label': lab}
	df = pd.DataFrame(df)
	df.to_csv('sampeltimeseries.csv')
	print('creat done')

if __name__ == '__main__':
	# creatsampel()
	filename = 'sampeltimeseries.csv'
	avser = [[]]
	ahser = [[]]
	label = []
	with open(filename) as f:
		reader = csv.reader(f)
		next(reader)
		for row in reader:
			tav = row[1][1:-1].split(', ')
			tah = row[2][1:-1].split(', ')
			ttav = []
			ttah = []
			for x in tav:
				ttav.append(float(x))
			for x in tah:
				ttah.append(float(x))
			avser.append(ttav)
			ahser.append(ttah)
			label.append(row[3])
	avser.pop(0)
	ahser.pop(0)
	print('read done')
	while True:
		key = input()
		while key not in ['downstairs', 'jog', 'sit', 'stand', 'upstairs', 'walk']:
			key = input('not in range')
		ti = input()
		ti = int(ti)
		for i in range(0, ti):
			row = random.randint(0, len(avser) - 1)
			while label[row] != key:
				row = random.randint(0, len(avser) - 1)
			ah = ahser[row]
			av = avser[row]
			plt.plot(ah, c=(1, 0, 0))#red
			plt.plot(av, c=(0, 1, 0))#green
			plt.title(key, fontsize=24)
			plt.axis([0, 100, -4.0, 4.0])
			plt.show()
