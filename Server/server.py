# coding:utf-8
from socket import socket, AF_INET, SOCK_DGRAM
import time
import math
import pickle
import numpy as np
import GetFeature
import tsfresh
import pandas as pd
from sklearn.externals import joblib
import _thread
from collections import Counter
import matplotlib.pyplot as plt


def getavah(list):
	ax, ay, az = list[1], list[2], list[3]
	gx, gy, gz = list[4], list[5], list[6]
	a2 = ax ** 2 + ay ** 2 + az ** 2
	g = math.sqrt(gx ** 2 + gy ** 2 + gz ** 2)
	av = ((ax * gx + ay * gy + az * gz) / g)
	ah = (math.sqrt(math.fabs(a2 - av ** 2)))
	av = av - g
	ah = ah
	return av, ah


class Udpsocket():
	def __init__(self):
		'''
		初始化，建立socket，ip端口绑定
		'''
		self.udpServerSocket = socket(AF_INET, SOCK_DGRAM)
		#         self.udpClientSocket = socket( AF_INET, SOCK_DGRAM )

		self.udpServerSocket.bind(('', 12333))  # 空串，表示监听所有ip
		self.buffer_size = 10240000  # 缓冲区大小
		self.plotbuffer = 0
		self.avqueue = []
		self.ahqueue = []
		self.dtanswer = []

	#         self.udpClientSocket.connect((u'10.41.5.103', 20179))

	def receive(self):
		'''
		收取端口传来的数据
		'''
		raw_data, addr = self.udpServerSocket.recvfrom(int(self.buffer_size))
		# print(raw_data)
		# print(addr)
		return raw_data, addr[0]

	def send(self, result, clientIp):
		'''
		返回信息
		'''
		host = clientIp
		port = 20120
		addr = (host, port)
		# self.udpServerSocket.sendto( str.encode(result), addr )#descriptor 'encode' requires a 'str' object but received a 'numpy.ndarray'
		self.udpServerSocket.sendto(str(result).encode(encoding="utf-8"), addr)

	#         self.udpClientSocket.sendto( result.encode(encoding="utf-8"), addr)
	def testdata(self, string):
		df = string.split(",")
		ret = np.ndarray(shape=(0, 9))
		for i in df:
			ret = np.append(ret, float(i))
		# ret = np.array(ret).reshape(1, -1)
		return [ret]

	def listen(self):
		'''
		监听端口，无限循环
		'''

		cnt = 0
		lines = []
		lasttime = int(time.time() * 1000)
		with open('../train/knn_model', 'rb') as fr:
			knn = pickle.load(fr)
		with open('../train/dt_model', 'rb') as fr:
			dt = pickle.load(fr)
		# with open('../train/svm_model', 'rb') as fr:
		# 	clf = pickle.load(fr)
		# knn = joblib.load("knn_model")
		# dt = joblib.load("dt_model")
		# gnb = joblib.load("gnb_model")

		while True:
			clientMsg, clientIp = self.receive()  # 接收数据
			if int(time.time() * 1000) - lasttime < 19:
				continue
			lasttime = int(time.time() * 1000)
			tmp = str(clientMsg)[2:-1]
			string = tmp
			df = string.split(",")
			ret = []
			for i in df:
				ret.append(float(i))
			# ret = np.array(ret).reshape(1, -1)
			# print(ret)
			tav, tah = getavah(ret)
			self.avqueue.append(tav)
			self.ahqueue.append(tah)
			while len(self.avqueue) > 100:
				self.avqueue.pop(0)
			while len(self.ahqueue) > 100:
				self.ahqueue.pop(0)
			if len(self.avqueue) != 100:
				continue
			self.plotbuffer += 1
			calcav = GetFeature.running_mean(self.avqueue)
			calcah = GetFeature.running_mean(self.ahqueue)
			fea = GetFeature.getfeature(calcav, calcah)
			yy = [19, 18, 17, 16, 15, 14, 12, 11, 10, 5, 4, 3, 2, 1]
			for x in yy:
				fea.pop(x)
			# answer_clf = clf.predict([fea])
			answer_clf = 1
			answer_knn = knn.predict([fea])
			answer_dt = dt.predict([fea])
			while len(self.dtanswer) > 10:
				self.dtanswer.pop(0)
			self.dtanswer.append(str(answer_dt)[2:-2])
			print(tav, tah, 'knn:', answer_knn, '    dt:', answer_dt)
			# print(int(answer_knn[0]))
			# 在这里对你服务器收到的数据做一定的操作，比如保存到某个数据结构中，完成加窗的操作，再调用你的算法模块
			# self.process( socket_data[1], socket_data[0] )  #处理接收的信息
			# 将你算法的结果返回，即替换下面这句里的"hahahah"
			cnt = cnt + 1

			self.send(answer_knn + '    ' + answer_dt, clientIp)
		# self.send(str(int(answer_knn[0]))+" "+str(int(answer_dt))+" "+str(int(answer_gnb)), clientIp)
		# print(str(cnt) + " " + str(int(answer_knn[0]))+" "+str(int(answer_dt))+" "+str(int(answer_gnb)) + " : " + tmp + " ")
		self.close()

	def close(self):
		'''
		关闭连接
		'''
		self.udpServerSocket.close()

	def __del__(self):
		self.close()

	def plot(self):
		while True:
			if self.plotbuffer > 200:
				plt.plot(self.ahqueue, c=(1, 0, 0))  # red
				plt.plot(self.avqueue, c=(0, 1, 0))  # green
				plt.title(Counter(self.dtanswer).most_common(1), fontsize=10)
				plt.axis([0, 100, -4.0, 4.0])
				plt.show()
				self.plotbuffer -= 20
				plt.close()


if __name__ == '__main__':
	print('start')
	# 实例化这个UDP类，并开启监听
	p = Udpsocket()
	# p.listen()
	print('creating thread')
	_thread.start_new_thread(p.listen, ())
	_thread.start_new_thread(p.plot, ())
	print('running')
