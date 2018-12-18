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
from io import StringIO
from lxml.html import parse
from threading import  Thread
import xml.etree.ElementTree as ET
from multiprocessing import Process

from Master import MisilaniousFunctions, SendFunctions, writeFunctions, SocketsMessage

try :
    import urllib.request
except :
    import urllib


class Restock(MisilaniousFunctions, SendFunctions, writeFunctions, SocketsMessage):

    def __init__(self):

        self.keyIndex = 0
        self.startTime = time.time()

        self.keyList = [ \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE','TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE']]

        authList = self.keyList[self.keyIndex]

        auth = tweepy.OAuthHandler(authList[0], authList[1])
        auth.set_access_token(authList[2], authList[3])

        self.api = tweepy.API(auth)

        self.fileName = 'RestockOverFlowSites.py'
        self.globalList = []

        with open(self.fileName, 'w+') as file :
            file.writelines('## OverFlow Functions Added Recently\n\ndef Server(self):\n\n')
            file.close()

        Process(target = self.runFunctions, args = ('RestockSites.py',)).start()

    def pageContentChange(self, url, imageURL, headers, timeout, name):

        checks = 0
        fails = 0
        name = (self.parseName(url) if name == '' else name)
        self.writeTxt('{}.out'.format(name.replace(' ', '-')), '{}\n\n{}\n\nStart time : {}\n\nTime elpased : none\n\nChecks : 0\n\nFails : 0\n\n'.format(time.time(), name, self.t()))

        sess = requests.Session()

        content = self.simpleGetReq(sess, url, headers, name)

        if content == 0:
            print ('Failed to get inital page content for {}, retrying in 1 minute'.format(url))
            time.sleep(60)
            self.pageContentChange(url, imageURL, headers, timeout, name)

        ogContent = content.content

        while True :
            update = False
            time.sleep(timeout)

            content = self.simpleGetReq(sess, url, headers, name)

            if content != 0 :
                checks += 1

                if ogContent != content.content:
                    self.tweetImageData('PAGE CHANGE\n{}\n{}'.format(name, url ), imageURL)
                    update = '{} updated at {}, status code {}\n\n'.format(url, self.t(), content.status_code)
                    ogContent = content.content

            else :
                fails += 1

            self.writePageChange(name, 0, checks, fails, update)

    def textRestock(self, url, image, selector, headers, timeout, name):

        count = 0
        fails = 0
        originalText = ''
        currentText = ''
        sess = requests.Session()
        name = (self.parseName(url) if name == '' else name)
        fileName = '{}.out'.replace(name.replace(' ', '-'))
        self.writeTxt(fileName, '{}\n\n{}\n\nStart time : {}\n\nTime elpased : none\n\nChecks : 0\n\nFails : 0\n\n'.format(time.time(), name, self.t()))

        content = self.simpleGetReq(sess, url, headers, name)

        if content == 0:
            print ('Failed to get {}, retrying in 1 minute'.format(url))
            time.sleep(60)
            self.textRestock(url, image, selector, headers, timeout, name)

        doc = parse(StringIO(content.text)).getroot()

        if selector != '':
            textHTML = doc.cssselect(selector)
            for t in textHTML:
                originalText += t.text_content()
        else :
            originalText = doc.text_content()

        while True :
            update = False
            time.sleep(timeout)

            content = self.simpleGetReq(sess, url, headers, name)

            if content == 0:
                currentText = originalText
                fails += 1
            else :
                doc = parse(StringIO(content.text)).getroot()
                if selector != '':
                    textHTML = doc.cssselect(selector)
                    for t in textHTML:
                        currentText += t.text_content()
                else :
                    currentText = doc.text_content()
                count += 1

            if currentText != originalText:

                self.tweetImageData( 'TEXT CHANGE\n{}\n{}'.format(title, url) , image)
                update = '{} updated at {}, status code {}\n\n'.format(url, self.t(), content.status_code)
                original = ''

                if selector != '':
                    textHTML = doc.cssselect(selector)
                    for t in textHTML:
                        originalText += t.text_content()
                else :
                    originalText = doc.text_content()

            currentText = ''

            self.writePageChange(fileName, 0, count, fails, update)
 
    def codeChange(self, url, image, headers, timeout, name) :

        count = 0
        fails = 0
        codeHist = []
        sess = requests.Session()
        name = (str(self.parseName(url)) if name == '' else  name)
        fileName = '{}.out'.format(name.replace(' ', '-'))
        self.writeTxt(fileName ,'{}\n\n{} : {}\n\nStarted at : {}\n\nTime elapsed : null\n\nChecks : 0\n\nFails : 0\n\nCode History : []'.format(time.time(), name, url, self.t()))

        request = self.simpleGetReq(sess, url, headers, name)

        if request == 0:
            self.codeChange(url, image, headers, timeout, name)

        oldScode = request.status_code
        codeHist.append(str(oldScode))

        while True :
            time.sleep(timeout)
            request = self.simpleGetReq(sess, url, headers, name)

            if request == 0:
                fails += 1
                newScode = oldScode
            else :
                count += 1
                newScode = request.status_code

            if newScode != oldScode:
                self.tweetImageData('{}\nStatus code update({}->{})\n{}'.format(name, oldScode, newScode, url), image)
                codeHist.append(str(newScode))
                oldScode = newScode

            count += 1

            self.writeScode(name, 0, url, count, fails, codeHist)

    def shopRestock(self, url, timeout):

        count = 0
        fails = 0
        dashCount = 0
        ogDict = {}
        curDict = {}
        reDict = {}
        sendList = []
        last430 = None
        restocks = False
        jLink = url + '.json'
        sess = requests.Session()

        for i in range(0, len(url)):
            if url[i] == '/':
                if dashCount == 2:
                    baseurl = url[0:i]
                    break
                else :
                    dashCount += 1

        name = url.replace(baseurl, '').replace('-', ' ').replace('.json', '').replace('/', ' ')
        baseurl += 'cart/add/'

        req = self.simpleGetReq(sess, jLink, {}, name)

        if req == 0 or req.status_code != 200:
            print ('Failed to load {}, status code {}, retrying in 1 minute'.format(jLink, req.status_code))
            time.sleep(60)
            self.shopRestock(url, timeout)

        self.writeTxt( '{}.out'.format(name.replace(' ', '-')) , '{}\n\nShopify Restock : {}\n\nStart time : {}\n\nTime elapsed : null\n\nChecks : 0\n\nFails : 0\n\nLast 430 : null\n'.format(time.time(), jLink, self.t(), ))

        Jdata = json.loads(req.text)
        productJson = json.loads(json.dumps(Jdata['product']))
        variantJson = json.loads(json.dumps(productJson['variants']))
        image = json.loads(json.dumps(json.loads(json.dumps(productJson['images']))[0]))['src'].replace('\/', '/')
        title = json.loads(json.dumps(productJson))['title']

        for j in variantJson:
            vJson = json.loads(json.dumps(j))
            if vJson['inventory_quantity'] != 0:
                ogDict.update( { vJson['title'] :  vJson['id'] } )

        while True :

            t1 = time.time()
            time.sleep(timeout)

            req = self.simpleGetReq(sess, jLink, {}, name)

            if req.status_code == 200:

                count += 1

                Jdata = json.loads(req.text)
                productJson = json.loads(json.dumps(Jdata['product']))
                variantJson = json.loads(json.dumps(productJson['variants']))

                curDict.clear()

                for j in variantJson:
                    vJson = json.loads(json.dumps(j))
                    if vJson['inventory_quantity'] != 0:
                        curDict.update( { vJson['title'] :  vJson['id'] } )

                if curDict.keys() != ogDict.keys():

                    reDict.clear()

                    restockSizes = list(set(curDict.keys()) - set(ogDict.keys()))
                    oosSizes = list( set(ogDict.keys()) - set(curDict.keys()) )

                    for i in oosSizes:
                        del ogDict[i]

                    for i in restockSizes:
                        reDict.update({ i : curDict[i] })

                    if restockSizes != []:

                        sizes = ', '.join(restockSizes)
                        restocks = '{} restocked at {}'.format(sizes, self.t())
                        text = '{}\n{}\n{}'.format(title, sizes, url )

                        t = self.tweetImageData(text, image)

                        if passed == True and t != False :

                            replyID = t.id
                            sendList[:] = []
                            sendString = ''
                            addLen = len('{}{}'.format(baseurl, curDict[restockSizes[0]] ))

                            for i in restockSizes:
                                if (len(sendString) + addLen) < 140:
                                    sendString += '{}{}\n'.format(baseurl, curDict[i])
                                else :
                                    sendList.append(sendString)
                                    sendString = ''

                            for i in sendList:
                                try :
                                    self.api.update_status(i, in_reply_to_status_id = replyID)
                                except :
                                    self.cycle()
                                    self.tellegramMessage('ERROR SENDING - {}'.format(sendList))
            else :
                fails += 1
                last430 = self.t()

            self.writeShopifyRestock(name, 0, count, fails, last430, restocks)
            restocks = False

    def meshCommerceRestock(self, site, pid):

        scrapeUrl = 'https://commerce.mesh.mx/stores/{}/products/{}'.format(site, pid)
        apiKey, userAgent, abrev = self.getMeshHeaders(site)

        headers = {
            'Host':'commerce.mesh.mx',
            'Connection':'keep-alive',
            'X-API-Key':apiKey,
            'Accept':'*/*',
            'X-Debug':'1',
            'Accept-Language':'en-us',
            'User-Agent':userAgent,
            'Accept-Encoding':'gzip, deflate',
            'MESH-Commerce-Channel':'iphone-app'}

        checks = 0
        fails = 0
        oldStock = []
        newStock = []
        restocks = []
        stockList = []
        sess = requests.Session()
        name = '{}:{}-restock.out'.format(site, pid)
        fileName = '{}.out'.format(name)
        self.writeTxt(fileName, '{}\n\n{} PID restock : {}\n\nStart Time : {}\n\nTime Elapsed : null\n\nChecks : 0\n\nFails : 0\n\nLast Check time\n\n'.format(time.time(), site, pid, self.t()))

        r = self.simpleGetReq(sess, scrapeUrl, headers, name)

        if r == 0 or r.status_code != 200:
            print ("Error starting {}, retrying in 1 minute".format(name))
            self.meshCommerceRestock(site, pid)

        data = json.loads(r.text)
        if data['oneSize'] == False :
            sizeData = json.loads(json.dumps(data['options']))
            for i in sizeData:
                d = json.loads(json.dumps(sizeData[i]))
                if d['stockStatus'] == 'IN STOCK':
                    oldStock.append(d['size'])

        else :
            if data['stockStatus'] == 'IN STOCK':
                oldStock.append("OS")

        while True :

            time.sleep(2)
            stockList[:] = []
            t1 = time.time()

            r = self.simpleGetReq(sess, scrapeUrl, headers, name)

            if r != 0 and r.status_code == 200 :

                checks += 1

                data = json.loads(r.text)
                if data['oneSize'] == False :
                    sizeData = json.loads(json.dumps(data['options']))
                    for i in sizeData:
                        d = json.loads(json.dumps(sizeData[i]))
                        if d['stockStatus'] == 'IN STOCK':
                            newStock.append(d['size'])
                else :
                    if data['stockStatus'] == 'IN STOCK':
                        newStock.append("OS")

                if newStock != oldStock :
                    restocks[:] = list( set(newStock) - set(oldStock) )
                    if len(restocks) > 0:
                        self.tweetImageData('{}\nSizes restocked : {}\n{}'.format(name, ','.join(restocks), url), image)
                    oldStock[:] = newStock
            else :
                fails += 1

            self.scrapeRestockWrite( fileName, 0, checks, time.time() - t1, fails, restocks)

    def barneyPIDrestock(self, pid ):

        headers = {
                'Host': 'www.barneys.com' ,
                'Connection': 'keep-alive'  ,
                'x-oc-client-id': 'FRIRgVKHoj1zkFoOqkwncsKE5Fc6ku2C' ,
                'Accept': '*/*' ,
                'User-Agent': 'Barneys/26 (iPhone; iOS 10.1.1; Scale/2.00)' ,
                'Accept-Language': 'en-US, en-us;q=0.8' ,
                'Authorization': 'Basic c3RvcmVmcm9udDpiYXJuZXlz' ,
                'Accept-Encoding': 'gzip, deflate' ,
        }

        checks = 0
        fails = 0
        oldStock = []
        newStock = []
        restocks = []
        stockList = []
        sess = requests.Session()
        name = 'barney-restock-{}'.format(pid)
        fileName = '{}.out'.format(name)
        scrapeUrl = 'https://www.barneys.com/rest/model/barneys/commerce/catalog/BNYProductDetailDisplayActor/getProductDetailsPageInfo?productId={}'.format(pid)
        self.writeTxt(fileName, '{}\n\nBarneys PID restock : {}\n\nStart Time : {}\n\nTime Elapsed : null\n\nChecks : 0\n\nFails : 0\n\nLast Check time\n\n'.format(time.time(), pid, self.t()))

        r = self.simpleGetReq(sess, scrapeUrl, headers, name)

        if r == 0 or r.status_code != 200:
            print ("Error starting {}, retrying in 1 minute".format(name))
            self.barneyPIDrestock(pid)

        data = json.loads(r.text)
        inventoryData = json.loads(json.dumps(data['inventoryDetails']))
        skuInventoryData = json.loads(json.dumps(inventoryData['skuInventoryStatus']))
        prodData = json.loads(json.dumps(data['productDetails']))
        prodData2 = json.loads(json.dumps(prodData[0]))
        atrData = json.loads(json.dumps(prodData2['attributes']))
        skuData = json.loads(json.dumps(skuInventoryData['skuInventoryATP']))

        image = atrData['product.auxImageURLS'][0][16:]
        name = atrData['product.displayName'][0]
        url = 'http://www.barneys.com/' + str(atrData['product.productDetailPageUrl'][0])

        sizes = atrData['sku.realSize']

        for sizeID, stock in skuData.items():
            stockList.append(stock)

        for size, stock in zip(sizes, stockList) :
            if stock > 0 :
                oldStock.append(size)

        while True :
            time.sleep(2)
            restocks[:] = []
            stockList[:] = []
            t1 = time.time()

            r = self.simpleGetReq(sess, scrapeUrl, headers, name)

            if r != 0 and r.status_code == 200 :

                checks += 1
                data = json.loads(r.text)
                inventoryData = json.loads(json.dumps(data['inventoryDetails']))
                skuInventoryData = json.loads(json.dumps(inventoryData['skuInventoryStatus']))
                prodData = json.loads(json.dumps(data['productDetails']))
                prodData2 = json.loads(json.dumps(prodData[0]))
                atrData = json.loads(json.dumps(prodData2['attributes']))

                skuData = json.loads(json.dumps(skuInventoryData['skuInventoryATP']))
                sizes = atrData['sku.realSize']

                for sizeID, stock in skuData.items():
                    stockList.append(stock)

                for size, stock in zip(sizes, stockList) :
                    if stock > 0 :
                        newStock.append(size)

                if newStock != oldStock :
                    restocks[:] = list( set(newStock) - set(oldStock) )

                    if len(restocks) > 0:
                        self.tweetImageData('{}\nSizes restocked : {}\n{}'.format(name, ','.join(restocks), url), image)
                    oldStock[:] = newStock

            else :
                fails += 1

            self.scrapeRestockWrite( fileName, 0, checks, time.time() - t1, fails, restocks)
