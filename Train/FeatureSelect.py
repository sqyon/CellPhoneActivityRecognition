#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import joblib
import pickle
# 导入预处理模块
from sklearn.preprocessing import Imputer
# 导入自动生成训练集和测试集的模块train_test_split
from sklearn.model_selection import train_test_split
# 导入预测结果评估模块classification_report
from sklearn.metrics import classification_report
# 从sklearn库中依次导入三个分类器模
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_selection import SelectKBest, chi2
import random
from sklearn.svm import SVC

# 数据导入函数,参数时特征文件的列表feature_paths和标签 文件的列表label_paths
# [21 ,20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
# yy = [21, 20, 19, 18, 17, 16, 15, 14, 11, 10, 7, 6, 3, 2, 1, 0]
yy = []

if __name__ == '__main__':
	dtreport=[]
	dtsave=[]
	for selectfea in range(1, 20):

		feature_path = ['new-nn.csv']
		label_paths = ['../RawDataProcessing/label.csv']
		print('Loading dataset')
		print('Spliting dataset')
		feature = np.ndarray(shape=(0, 20 - len(yy)))
		label = np.ndarray(shape=(0, 1))
		for file in feature_path:
			df = pd.read_csv(file)
			for x in yy:
				df.drop(df.columns[x], axis=1, inplace=True)
			imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
			imp.fit(df)
			df = imp.transform(df)
			feature = np.concatenate((feature, df))
		for file in label_paths:
			df = pd.read_csv(file)
			label = np.concatenate((label, df))
		label = np.ravel(label)
		x_read, y_read = feature, label

		X_chi2 = SelectKBest(chi2, k=selectfea).fit_transform(x_read, y_read)

		x_all, x_, y_all, y_ = train_test_split(X_chi2, y_read, test_size=0.0)
		x_train, y_train, x_test, y_test = np.ndarray(shape=(0, len(x_all[0]))), np.array([]), np.ndarray(
			shape=(0, len(x_all[0]))), np.array([])

		testlen = 100000
		x_test = np.concatenate((x_test, x_all[len(x_all) - testlen:, :]), 0)
		y_test = np.concatenate((y_test, y_all[len(x_all) - testlen:]), 0)
		x_train = np.concatenate((x_train, x_all[:len(x_all) - testlen, :]), 0)
		y_train = np.concatenate((y_train, y_all[:len(x_all) - testlen]), 0)

		print("Start training DT")
		dt = DecisionTreeClassifier().fit(x_train, y_train)
		dtsave.append(dt)
		with open('dt_model', 'wb') as fw:
			pickle.dump(dt, fw)
		# joblib.dump(dt, "dt_model")
		print("Training done!")
		answer_dt = dt.predict(x_test)
		print("\n\nThe classifiction report for dt with", selectfea,'features:')
		dtreport.append(classification_report(y_test, answer_dt))
		print(dtreport[-1])
	exit(0)
