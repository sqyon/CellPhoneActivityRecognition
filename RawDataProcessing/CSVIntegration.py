import os
import csv
import math
import pandas as pd
import numpy as np
import GetFeature

if __name__ == '__main__':
	rawdata = './SelectedDataset'
	files = os.listdir(rawdata)  # 得到文件夹下的所有文件名称
	gx, gy, gz = [], [], []
	ax, ay, az = [], [], []
	av, ah = [], []
	label = []
	for file in files:  # 遍历文件夹
		if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
			print('reading ' + str(file))
			with open(rawdata + "/" + file) as f:
				reader = csv.reader(f)
				next(reader)
				for row in reader:
					gx.append(float(row[4]))
					gy.append(float(row[5]))
					gz.append(float(row[6]))
					ax.append(float(row[10]))
					ay.append(float(row[11]))
					az.append(float(row[12]))
					a2 = ax[-1] ** 2 + ay[-1] ** 2 + az[-1] ** 2
					g = math.sqrt(gx[-1] ** 2 + gy[-1] ** 2 + gz[-1] ** 2)
					av.append((ax[-1] * gx[-1] + ay[-1] * gy[-1] + az[-1] * gz[-1]) / g - g)
					ah.append(math.sqrt(math.fabs(a2 - av[-1] ** 2)))
					av[-1] = av[-1] + 1.0
					ah[-1] = ah[-1] - 1.0
					if str(file[:3]) == 'dow':
						label.append('downstairs')
					elif str(file[:3]) == 'jog':
						label.append('jog')
					elif str(file[:3]) == 'sit':
						label.append('sit')
					elif str(file[:3]) == 'sta':
						label.append('stand')
					elif str(file[:3]) == 'ups':
						label.append('upstairs')
					elif str(file[:3]) == 'wal':
						label.append('walk')
	print('read done, creating dataframe')
	df = pd.DataFrame({'av': av, 'ah': ah, 'label': label})
	print('datafram created, exporting')
	df.to_csv('rawdata.csv')
	print('exporting done')

	feed = [[]]
	feature, lab = [], []
	steplen = 100
	for i in range(0, len(av) - steplen):

		if (i % 200 == 0):
			print('feature ', i, '/', len(av))

		flag = False
		for j in range(0, steplen):
			if label[i + j] != label[i]:
				flag = True
		if flag:
			continue
		tav, tah = [], []
		for j in range(0, steplen):
			tav.append(av[i + j])
			tah.append(ah[i + j])
		tav = GetFeature.running_mean(tav)
		tah = GetFeature.running_mean(tah)
		fea = GetFeature.getfeature(tav, tah)

		# avser.append(str(tav))
		# ahser.append(str(tah))
		feature.append(str(fea))
		lab.append(label[i])
		feed.append(fea)
	if len(feed[0]) == 0:
		feed.pop(0)
	print('feature done, creating dataframe')
	df = pd.DataFrame(feed)
	df.to_csv('feeddata.csv', index=False)
	df = pd.DataFrame(lab)
	df.to_csv('label.csv', index=False)
	print('all done')
	# df = pd.DataFrame({'avser': avser, 'ahser': ahser, 'feature': feature, 'label': lab})
	# print('datafram created, exporting')
	# df.to_csv('dataset.csv')
