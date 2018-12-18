import time
import tweepy
import requests
from io import StringIO
from lxml.html import parse

from Master import MisilaniousFunctions, SendFunctions, writeFunctions, SocketsMessage


class ScrapeFunctions:

    def createPIDlist(self, start, stop, pidFile):
        new = []
        old = []

        if start == 0:
            Zs = ['00000', '0000', '000', '00', '0']
            for i in range(0, 100000):
                z = Zs[len(str(i)) - 1]
                new.append('{}{}'.format(z, i))
        else:
            for i in range(start, stop + 1):
                new.append(str(i))

        with open(pidFile, 'r') as file:
            for i in file.readlines():
                old.append(str(i).replace('\n', ''))

        return list(set(new) - set(old))

class Scrape(MisilaniousFunctions, SendFunctions, writeFunctions, SocketsMessage, ScrapeFunctions):

    def __init__(self):

        self.keyList = [ \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE','TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE']]

        self.keyIndex = 0
        self.startTime = time.time()

        authList = self.keyList[self.keyIndex]

        auth = tweepy.OAuthHandler(authList[0], authList[1])
        auth.set_access_token(authList[2], authList[3])

        self.api = tweepy.API(auth)

    def meshImageScrape(self, site, start, stop):

        abrevDict = {
            'footpatrol' : 'fp',
            'size' : 'sz',
            'JDsports' : 'jd',
            'Tessuti' : 'te'
        }

        count = 0
        fails = 0
        failList = []
        tempPids = []
        pidList = []
        sess = requests.Session()
        abreviation = abrevDict[site]
        name = '{}-{}:{}'.format(site, start, stop)
        pidFile = '{}-pids.out'.format(site)
        fileName = "{}:{}-{}.out".format(site, start, stop)
        self.scrapeImageWrite(fileName, 0, start, stop, 0, 0, 0, [])

        pidList = self.createPIDlist(start, stop, pidFile)

        while True :

            for i in pidList:

                t1 = time.time()
                r = self.simpleGetReq(sess, 'http://i1.adis.ws/i/jpl/{}_{}_a?w=1&h=1'.format(abreviation, i), {}, name)
                t2 = time.time()

                if r != 0 :
                    count += 1
                    if r.status_code == 200 :
                        self.tweetImageData('New product ({}) loaded on {}'.format(i, site), 'http://i1.adis.ws/i/jpl/{}_{}_a?w=1000&h=1000'.format(abreviation, i))
                        self.appendTxt(pidFile, i)
                        pidList.remove(i)
                else :
                    fails += 1
                    failList.append(i)

                self.scrapeImageWrite(fileName, 0, start, stop, count, t2 - t1, fails, failList)

            #count += 1
            #self.scrapeImageWrite(fileName, 0, start, stop, count, time.time() - t1, fails, failList)

    def barneyImageScrape(self, start, stop ):

        count = 0
        fails = 0
        pidList = []
        tempPids = []
        pidFails = []
        sess = requests.Session()
        name = 'Barneys-IMG-scrape-{}:{}'.format(start, stop)
        fileName = '{}.out'.format(name)
        self.scrapeImageWrite(fileName, 0, start, stop, count, 0, fails, [])

        pidList = self.createPIDlist(start, stop, 'barneys-pids.out')

        while True :

            for i in pidList:

                t1 = time.time()

                r = self.simpleGetReq(sess, 'https://product-images.barneys.com/is/image/Barneys/{}'.format(i), {}, name)

                if (r != 0):
                    count += 1
                    if (r.status_code == 200) :
                        pidList.remove(str(i))
                        self.appendTxt('barneys-pids.out', i)
                        print ('[{}] : Barneys pid found {}'.format(self.t(), i))
                        self.tweetImageData('New product ({}) loaded on www.barneys.com'.format(i), 'https://product-images.barneys.com/is/image/Barneys/{}'.format(i))

                else :
                    pidFails.append(i)
                    fails += 1

                self.scrapeImageWrite(fileName, 0, start, stop, count, time.time() - t1, fails, pidFails)

    def mrPorterImageScrape(self, start, stop, pidFile):

        count = 0
        fails = 0
        failList = []
        tempPids = []
        sess = requests.Session()
        name = 'MrPorter---{}:{}'.format(start, stop)
        fileName = "{}.out".format(name)
        self.scrapeImageWrite(fileName, 0, start, stop, 0, 0, 0, [])

        pidList = self.createPIDlist(start, stop, pidFile)

        while True :

            for i in pidList:

                t1 = time.time()
                r = self.simpleGetReq(sess, 'https://cache.mrporter.com/images/products/{}/{}_mrp_fr_l.jpg'.format(i, i), {}, name)
                t2 = time.time()

                if r != 0 :
                    count += 1
                    if r.status_code == 200 :
                        self.tweetImageData('New product ({}) loaded on Mr Porter'.format(i), 'https://cache.mrporter.com/images/products/{}/{}_mrp_fr_l.jpg'.format(i, i))
                        self.appendTxt(pidFile, i)
                        pidList.remove(i)
                else :
                    fails += 1
                    failList.append(i)

                self.scrapeImageWrite(fileName, 0, start, stop, count, t2 - t1, fails, failList)

    def doverStreetMarketUrlScrape(self, start, stop, local):

        s = requests.Session()

        t1 = time.time()

        if local == 'japan':
            url = 'https://shop.doverstreetmarket.com/jp/index/asics-tiger'
        elif local == 'london':
            url = 'https://shop.doverstreetmarket.com/index/vans'
        elif local == 'usa':
            url = 'https://shop.doverstreetmarket.com/us/sneaker-space/common-projects-2'
        elif local == 'singapore':
            url = 'https://shop.doverstreetmarket.com/sg/index/common-projects'

        r = requests.get(url)
        doc = parse(StringIO(r.text)).getroot()
        productUrl = doc.cssselect('li.item a').get('href')
        r = requests.get(productUrl)
        doc = parse(StringIO(r.text)).getroot()
        keyUrl = str(doc.cssselect('div.product-essential form').get('action'))
        formKey = keyUrl[66:len(keyUrl) - 15]

        filename = "DSM--{}:{}.out".format(start, stop)
        with open(filename, 'w+') as file:
            file.write('Form key --- {}\n\n\n'.format(formKey))
            file.close()

        for i in range(start, stop + 1):
            r = self.simplePostReq(s, 'https://shop.doverstreetmarket.com/checkout/cart/addmulti/uenc/{}/product/{}/'.format(formKey, i), {'product': str(i)}, {}, "DSM" )

            if r.status_code == 200:
                if '/checkout/cart/' not in r.url:
                    self.appendText('{} ---- {}\n\n'.format(i, r.url))
            elif r.status_code == 429:
                print ('{} - DSM {} 429 error sleeping for 3 minutes....'.format(self.t(), local))
                time.sleep(180)
                print ('{} - DSM {} done sleeping, resuming scraping, starting with PID {}'.format(self.t(), local, i))
            elif r.status_code == 403:
                print ('{} - DSM {} 403 error stopped scraping with PID {}'.format(self.t(), local, i))
                break


        t2 = time.time()

        self.appendText('\n\n\nTotal scrape time - {} seconds\nAverage request time - {} seconds'.format(t2 - t1,(t2 - t1) / (stop - start + 1)))

