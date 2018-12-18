import cv2
import time
import shutil
import requests
import numpy as np
from multiprocessing import Process

class meshScrape:

	def __init__(self):

		shutil.copyfileobj( requests.get('https://i1.adis.ws/t/jpl/sz_product_list?plu=sz_281641_a&qlt=80&w=300&h=337&v=1', stream = True).raw,  open('STOCK_IMG.jpg', 'wb') )

		for i in ['Size.out', 'JDsports.out', 'Tessuti.out']:
			with open(i, 'w+') as file :
				file.close()

	def download(self, sess, imgURL):
		try :
			r = sess.get(imgURL, stream = True).raw
			shutil.copyfileobj( r,  open('CUR_IMG.jpg', 'wb') )
			passed = True
		except :
			passed = False

		return passed

	def scrape(self, start, stop):

		pids = []
		pidAP = pids.append

		for site in ['sz', 'jd', 'te']:

			pids[:] = []

			if site == 'sz':
				fileName = 'Size.out'
			elif site == 'jd':
				fileName = 'JDsports.out'
			elif site == 'te':
				fileName = 'Tessuti.out'

			sess = requests.Session()

			for i in range(start, stop):
				if self.download(sess, 'https://i1.adis.ws/t/jpl/sz_product_list?plu={}_{}_a&qlt=80&w=300&h=337&v=1'.format(site, i)) == True :
					dif = cv2.subtract(cv2.imread('STOCK_IMG.jpg'), cv2.imread('CUR_IMG.jpg'))
					if np.any(dif) == True :
						pidAP(str(i))

		with open(fileName, 'a') as file :
			file.writelines('\n'.join(pids))
			file.close()


	def parseLine(self, line, n, string):
	    if len(line) >= n + 6:
	        string += '{}\n'.format(line[n:n+6])
	        return parseLine(line, n+6, string)
	    else :
	        return string

	def fixerooo(self, fileName, finalFileName):
	    with open(fileName, 'r') as file:
	        data = file.readlines()
	        file.close()

	    for i in range(0, len(data)):
	        line = (str(data[i]))
	        if len(line) > 6:
	            data[i] = self.parseLine(line, 0, '')

	    with open(finalFileName, 'w+') as file :
	        file.writelines(data)
	        file.close()

	def __del__(self):
		for i in ["Size", "JDsports", "Tessuti"]:
			self.fixerooo('{}.out'.format(i), '{}-fix.out'.format(i))

i = meshScrape()

for n in range(200000, 299999, 5000):
	Process(target=i.scrape, args=(n, n+5000,)).start()
