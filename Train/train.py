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
import random
from sklearn.svm import SVC

# 数据导入函数,参数时特征文件的列表feature_paths和标签 文件的列表label_paths
# [19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
yy = [19, 18, 17, 16, 15, 14, 12, 11, 10, 5, 4, 3, 2, 1]


def load_dataset(feature_path, label_paths):
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
	return feature, label


if __name__ == '__main__':
	featurePaths = ['../RawDataProcessing/feeddata.csv']
	labelPaths = ['../RawDataProcessing/label.csv']
	print('Loading dataset')
	x_read, y_read = load_dataset(featurePaths, labelPaths)
	print(len(x_read), len(y_read))
	print('Spliting dataset')
	knnreport = []
	dtreport = []
	for _ in range(0, 1):

		x_train, x_test, y_train, y_test = train_test_split(x_read, y_read, test_size=1.0, )

		print('Dataset loaded')
		print('Feature len = ', len(x_train[0]))
		print('Train len = ', len(x_train))
		print('Test len = ', len(x_test))

		# print("Start training clf")
		# clf = SVC(gamma='auto')
		# clf.fit(x_train, y_train)
		# with open('svm_model', 'wb') as fw:
		# 	pickle.dump(clf, fw)
		# print("Training done!")

		print("Start training knn")
		knn = KNeighborsClassifier().fit(x_train, y_train)
		with open('knn_model', 'wb') as fw:
			pickle.dump(knn, fw)
		print("Training done!")
		print("Start training DT")
		dt = DecisionTreeClassifier().fit(x_train, y_train)
		with open('dt_model', 'wb') as fw:
			pickle.dump(dt, fw)
		# joblib.dump(dt, "dt_model")
		print("Training done!")
		# print("Start training Bayes")
		# gnb = GaussianNB().fit(x_train, y_train)
		# with open('gnb_model', 'wb') as fw:
		# 	pickle.dump(gnb, fw)
		# print("Training done!")

		print('Predicting')
		# answer_clf = clf.predict(x_test)
		answer_knn = knn.predict(x_test)
		answer_dt = dt.predict(x_test)
		# answer_gnb = gnb.predict(x_test)
		print("Prediction done")
		print('The', _, '-th train and test report:')
		# 计算准确率与召回率
		# print("\n\nThe classifiction report for clf:")
		# print(classification_report(y_test, answer_clf))
		print("\n\nThe classifiction report for knn:")
		knnreport.append(classification_report(y_test, answer_knn))
		print(knnreport[-1])
		print("\n\nThe classifiction report for dt:")
		dtreport.append(classification_report(y_test, answer_dt))
		print(dtreport[-1])
		# print("\n\nThe classifiction report for gnb:")
		# print(classification_report(y_test, answer_gnb))
