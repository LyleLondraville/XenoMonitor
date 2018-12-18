import os
import json
import time
import shutil
import random
import tweepy
import smtplib
import requests
import datetime
import unicodedata
try:
    import urllib.request
except :
    pass
 
from io import StringIO
from lxml.html import parse
from threading import  Thread
from multiprocessing import Process
 
import xml.etree.ElementTree as ET

from Master import MisilaniousFunctions, SendFunctions, writeFunctions, SocketsMessage


class StockPriceMonitor(MisilaniousFunctions, SendFunctions, writeFunctions, SocketsMessage):

    def __init__(self):

        self.keyIndex = 0
        self.updates = []
        self.hasteShoes = ''
        self.shoes = []
        self.currLen = 0

        self.keyList = [ \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE','TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE']]

        authList = self.keyList[self.keyIndex]

        auth = tweepy.OAuthHandler(authList[0], authList[1])
        auth.set_access_token(authList[2], authList[3])

        self.api = tweepy.API(auth)

        Process(target = self.tweetSumary, args = ()).start()

        self.fileName = 'StockOverFlowSites.py'
        self.globalList = []
        self.names = []

        with open(self.fileName, 'w+') as file :
            file.writelines('## OverFlow Functions Added Recently\n\ndef Server(self):\n\n')
            file.close()

        with open("StockXNames.out", 'w+') as file :
            #file.writelines('')
            file.close()



        Process(target = self.runFunctions, args = ('StockPriceSites.py',)).start()
        Process(target = self.tweetSumary, args = ()).start()
        

    def searchStockX(self, phrase):

        results = []

        searchHeaders = {
            'Host': 'xw7sbct9v6-dsn.algolia.net',
            'Connection': 'keep-alive',
            'accept': 'application/json',
            'Origin': 'https://stockx.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://stockx.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8'}

        query = 'query={}&hitsPerPage=20&facets=*'.format(phrase.replace(' ', '%20'))
        jPostData = json.dumps({'params' : query})
        search = requests.post('https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.22.1&x-algolia-application-id=XW7SBCT9V6&x-algolia-api-key=6bfb5abee4dcd8cea8f0ca1ca085c2b3', data = jPostData, headers = searchHeaders)
        searchJson = json.loads(search.text)['hits']


        for J in searchJson:
            jsonData = json.loads(json.dumps(J))
            name = jsonData['name']
            pid = jsonData['style_id']
            #image = jsonData['thumbnail_url']
            url = 'https://stockx.com/api/products/{}/activity?state=480'.format(jsonData['objectID'])
            results.append('Process(target = self.stockX, args = ("{}", "{} : {}")).start()'.format(url, name.replace('"', ''), pid))

        for i in results:
            print(i)
 
    def getStockXPackage(self, url):

        jLoads = json.loads
        jDumps = json.dumps

        for i in range(len(url) - 1, -1, -1):
            if url[i] == '/' and i != len(url) - 1:
                phrase = url[i+1:].replace('-', ' ').replace('/', '')
                break

        searchHeaders = {
            'Host': 'xw7sbct9v6-dsn.algolia.net',
            'Connection': 'keep-alive',
            'accept': 'application/json',
            'Origin': 'https://stockx.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://stockx.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8'}

        query = 'query={}&hitsPerPage=20&facets=*'.format(phrase.replace(' ', '%20'))
        jPostData = jDumps({'params' : query})
        search = requests.post('https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.22.1&x-algolia-application-id=XW7SBCT9V6&x-algolia-api-key=6bfb5abee4dcd8cea8f0ca1ca085c2b3', data = jPostData, headers = searchHeaders)
        searchJson = jLoads(search.text)['hits']

        if len(searchJson) > 0:
            jsonData = jLoads(jDumps(searchJson[0]))
            name = jsonData['name']
            searchable_traits = jLoads(jDumps(jsonData['searchable_traits']))
            pid  = jLoads(jDumps(searchable_traits['Style']))
            prodURL = 'https://stockx.com/api/products/{}/activity?state=480'.format(jsonData['objectID'])
            package = [prodURL, '{} : {}'.format(name, pid)]
        else :
            package = []

        return package

    def getStockXdata(self, url):
        
        headers = {
            'Host': 'stockx.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'appVersion': '0.1',
            'appOS': 'web',
            'X-Requested-With':'XMLHttpRequest',
            'JWT-Authorization': 'false',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'en-US,en;q=0.8'} 

        try :
            r = requests.get(url, headers = headers)
            if r.status_code != 200:
                print ("status code error retreving {} got {} at {}".format(url, r.status_code, self.t()))
                self.getStockXdata(url)
            else :
                return r
        except :
            print ("Error retreaving {}, time : {}".format(url, self.t()))

    def stockX(self, url, name):

        oldSum = 0
        count = 0
        days = 1
        self.shoes.append(name)

        fileName = '{}.out'.format(name.replace(' ', '-').replace('(', '').replace(')', ''))

        jsonData = json.loads((self.getStockXdata(url)).text)

        while len(jsonData) == 0:
            print ('[ {} ] : no sales yet, waiting 4 hours'.format(name))
            time.sleep(60*60*4)
            jsonData = json.loads((self.getStockXdata(url)).text)

        for i in jsonData:
            price = float(json.loads(json.dumps(i))['amount'])
            oldSum += price

        oldMarket = round(oldSum/float(len(jsonData)), 2)

        self.appendTxt('StockXNames.out', '{} : {}$\n'.format(name, oldMarket) )
        self.writeTxt(fileName, '{}\n\n{}\n{}\nOriginal Price {}\n\nStart Time : {}\n\nTime Elapsed : null\n\nChecks : 0\n\nChanges\n'.format(time.time(), name, url, oldMarket, self.t() ))

        while True :
            time.sleep(86400)
            newSum = 0

            jsonData = json.loads(self.getStockXdata(url)).text
            count += 1

            for i in jsonData:
                price = float(json.loads(json.dumps(i))['amount'])
                newSum += price

            newMarket = round(newSum/float(len(jsonData)), 2)
            try :
                change = ((newMarket/oldMarket)-1)*100
            except :
                print (jsonData)
                print (len(jsonData))
                break 

            self.writeStockX(fileName, 0, count, '\t[{}] : {}% change, average selling price of {}\n'.format(self.t(), change, newMarket) )
            self.updatePrice(name, '{} : {}$\n'.format(name, newMarket))

            if change >= 105 or change <= 95:
                self.updates.append('{} : {}% change over {} day(s)\n'.format(name, newMarket, change, days))
                oldMarket = newMarket
                days = 1
            else :
                days += 1

    def updatePrice(self, name, new):
        
        with open('StockXNames.out', 'r') as file :
            data = file.readlines()
            file.close()

        for i in range(0, len(data)):
            if name in data[i]:
                data[i] = new
                break 

        with open('StockXNames.out', 'w') as file :
            file.writelines(data)
            file.close()

    '''
    def returnStockHaste(self, tID):
        sendData = []
        with open('StockXNames.out', 'r') as file :
            data = file.readlines()
            file.close()

        for i in range(0, len(data)):
            data[i] = data[i].replace('\n', '')
            if data[i] != '':
                sendData.append(data[i])
        
        
        if (len(self.shoes) > self.currLen):
            i = self.makeHaste('\n'.join(self.shoes))
            if i != False :
                self.hasteShoes = i
                self.currLen = len(self.hasteShoes)
                self.tweetDM(int(tID), 'Here is a list of the items currently being monitored for changes in price by Xeno Monitor {}'.format(self.hasteShoes))
            else :
                self.tweetDM(int(tID), "Sorry but a list of the shoes currently being monitored for in price is not avalable right now, please try again in a hour")
                
        else :
            try :
                r = requests.get(self.hasteShoes)
                if r.status_code == 200 :
                    self.tweetDM(int(tID), 'Here is a list of the items currently being monitored for changes in price by Xeno Monitor {}'.format(self.hasteShoes))
                elif r.status_code == 404:
                    i = self.makeHaste('\n'.join(self.shoes))
                    if i != False :
                        self.hasteShoes = i
                        self.currLen = len(self.hasteShoes)
                        self.tweetDM(int(tID), 'Here is a list of the items currently being monitored for changes in price by Xeno Monitor {}'.format(self.hasteShoes))
                    else :
                        self.tweetDM(int(tID), "Sorry but a list of the shoes currently being monitored for in price is not avalable right now, please try again in a hour")
                else :
                    self.tweetDM(int(tID), "Sorry but a list of the shoes currently being monitored for in price is not avalable right now, please try again in a hour")
            except Exception as e:
                print (e)
                self.tweetDM(int(tID), "Sorry but a list of the shoes currently being monitored for in price is not avalable right now, please try again in a hour")

    '''

        

    def tweetSumary(self):

        time.sleep(60*10)

        while True :
            time.sleep(86400)
            if self.updates != []:
                now = datetime.datetime.now()
                date = '{}/{}/{} {} : {} : {}\n\n'.format(now.month, now.day, now.year, now.hour, now.minute, now.second)

                self.writeTxt('{}-{}:{}.out'.format(now.year, now.month, now.day), date + ''.join(self.updates) )
                jData = json.dumps(date + ''.join(self.updates))

                self.updates[:] = []

                self.tweetRegular('Daily Sneaker Market Summary\n{}'.format(self.makeHaste(jData)))
            else :
                pass














