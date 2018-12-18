import json
import random
import time
import tweepy
import requests
from multiprocessing import Process

import xml.etree.ElementTree as ET


from Master import MisilaniousFunctions, SendFunctions, writeFunctions


class shopy(MisilaniousFunctions, SendFunctions, writeFunctions): 
    
    def __init__(self):

   
        self.keyIndex = 0
        self.startTime = time.time()
        Process(target = self.clearImages, args = ()).start()

        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        self.keyList = [ \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE','TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE']]

        authList = self.keyList[self.keyIndex]
        auth = tweepy.OAuthHandler(authList[0], authList[1])
        auth.set_access_token(authList[2], authList[3])
        self.api = tweepy.API(auth)
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#



        ips = ['45.76.251.33',
                   '45.76.250.14',
                   '45.76.63.109',
                   '108.61.215.117',
                   '104.156.254.55',
                   '173.230.154.252',
                   '173.255.211.105',
                   '96.126.101.171',
                   '192.155.80.236',
                   '192.81.128.7',
                   '23.92.24.143',
                   '23.239.4.220',
                   '45.56.92.162',
                   '45.33.36.11',
                   '45.33.44.247',
                   '45.33.52.54',
                   '45.33.60.244',
                   '45.33.108.199',
                   '192.81.134.242',
                   '45.56.88.104'
                    ]

      
        for i in ips:
            try :
                requests.get('https://shop.bdgastore.com/', proxies = {'https':'https://{}:{}'.format(i, 3128)})
            except :
                print ('Errror in Proxy {}'.format(i))



        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


    def rotateProx(self, pos, proxies, nadaIPS):

        if pos != len(proxies)-1:
            p = pos+1

        else :
            p = 0

        for x,y in nadaIPS.items():
            if p == x:
                if time.time()-y >= 150:
                    del nadaIPS[p]
                    return p, nadaIPS
                else :
                    self.rotateProx(p, proxies, nadaIPS)

        return p, nadaIPS

    def shopGet(self, url, name, proxies, nadaIPS, pos):

        proxy = {'https':'https://{}:{}'.format(proxies[pos], random.randint(3110, 3128))}
        p, nadaIPS = self.rotateProx(pos, proxies, nadaIPS)

        try :
            r = requests.get(url, proxies = proxy)
            rcode = r.status_code

            if rcode == 200:
                return r, p, nadaIPS

            else :
                nadaIPS.update({pos:time.time()})
                self.writeReqError('{}.out'.format(name.replace(' ', '-')),0,rcode)
                print ('{} - {} error {}'.format(url, rcode, proxy))

                if len(nadaIPS) == len(proxies):
                    print("{} Resting ips...".format(self.t()))
                    time.sleep(150)
                    nadaIPS.clear()

                return self.shopGet(url, name, proxies, nadaIPS, p)

        except Exception as e:
            time.sleep(1)
            self.writeReqError('{}.out'.format(name.replace(' ', '-')), 0, 0)
            print("Shopify error retrieving {} at {}\nerror - {}".format(url, self.t(), e))
            return self.shopGet(url, name, proxies, nadaIPS, p)

    def tweetShopifyReply(self, url, name, title, image, jsonSelectorOption):

        tID = self.tweetImageData( '{}\n{}'.format(title, url), image )
        dashCount = 0
        string = ''

        if tID != False :
            addlist = []
            replylist = []

            for i in range(0, len(url)):
                if url[i] == '/':
                    if dashCount == 2:
                        baseurl = url[0:i+1]
                        break
                    else :
                        dashCount += 1

            baseurl += 'cart/add/'


            r = self.getReq(requests.Session(), '{}.json'.format(url), {}, name)
            productJSON = json.loads(r.text)['product']
            varJSON = json.loads(json.dumps(productJSON['variants']))

            try :
                int(varJSON[0]['inventory_quantity'])
                checkStock = True
            except :
                checkStock = False

            if checkStock == False :
                for i in varJSON:
                    addUrl = '{} - {}{}\n'.format(str(i[jsonSelectorOption]), baseurl, str(i['id']))
                    addlist.append(addUrl)

            else :
                for i in varJSON:
                    if int(i['inventory_quantity']) > 0:
                        addUrl = ('{} - {}{}\n').format(str(i[jsonSelectorOption]), baseurl, str(i['id']))
                        addlist.append(addUrl)

            if addlist != []:

                itemLen = len(addlist[0])

                for i in addlist:
                    if (len(string) + itemLen) <= 140 :
                        string += i
                    else :
                        replylist.append(string)
                        string = ''
                        string += i

                replylist.append(string)

                for i in replylist:
                    time.sleep(.25)

                    try :
                        self.api.update_status(i, in_reply_to_status_id = str(tID.id))
                    except :
                        time.sleep(1.5)
            else :
                print ('Nothing to reply to - {}'.format(url))
        else :
            print ('Error Replying to {}'.format(url))

    def superShopify(self, url, filter, proxyPool, jsonSelectorOption, timeout, name):

        self.writeFile(name)
        initalTime = time.time()

        count = 0
        pos = random.randint(0, len(proxyPool)-1)
        old = []
        nadaIPS = {}
        oldAppend = old.append
        sitemapUrl = '{}sitemap_products_1.xml?'.format(url)
   
        oldCntnt, pos, nadaIPS = self.shopGet(sitemapUrl, name, proxies, nadaIPS, pos)
        oldRoot = ET.fromstring(oldCntnt.content)

        for i in oldRoot:
            oldChild = i.getchildren()
            link = oldChild[0].text
            oldAppend(link)

        while True:

            newCntnt = None
            newRoot = None

            if time.time() - initalTime >= 3600:

                old[:] = []

                oldCntnt, pos, nadaIPS = self.shopGet(sitemapUrl, name, proxies, nadaIPS, pos)
                oldRoot = ET.fromstring(oldCntnt.content)

                for i in oldRoot:
                    oldChild = i.getchildren()
                    link = oldChild[0].text

                    oldAppend(link)

                initalTime = time.time()

            else :
                pass

            time.sleep(timeout)

            t1 = time.time()

            
            newCntnt, pos, nadaIPS = self.shopGet(sitemapUrl, name, proxies, nadaIPS, pos)

            try :
                newRoot = ET.fromstring(newCntnt.content)
                passed = True

            except :
                print (('[{}] : lxml error, retrying').format(name))
                passed = False

            if passed == True :

                for i in newRoot:
                    newChild = i.getchildren()
                    link = newChild[0].text

                    if link not in old :
                        try :
                            newChild2 = (newChild[3]).getchildren()
                            title = self.normalizeText(newChild2[1].text)
                            image = newChild2[0].text

                        except :
                            title = self.parseName(link)
                            image = ''

                        if filter == True :

                            if self.filter('{}{}{}'.format(title, image, link)) == True and jsonSelectorOption != "":
                                self.tweetShopifyReply(link, title, proxies, image, jsonSelectorOption)
                            else :
                                self.tweetImageData('{}\n{}'.format(title, link), image)

                        
                        else :
                            if self.filter('{}{}{}'.format(title, image, link)) == True  and jsonSelectorOption != "":
                                self.tweetShopifyReply(link, title, proxies, image, jsonSelectorOption)
                            else :
                                self.tweetImageData('{}\n{}'.format(title, link), image)

                        old.append(link)

                count +=1 
                self.writeUpdate(0, name, len(old), newCntnt.status_code, round((time.time()-t1), 2), count)
            
            else :
                pass

    def shopify(self, url, filter, timeout, jsonSelectorOption, name):

        self.writeFile(name)
        initalTime = time.time()

        count = 0
        old = []
        oldAppend = old.append
        s = requests.Session()
        sitemapUrl = '{}sitemap_products_1.xml?'.format(url)

        oldCntnt  = self.getRequ(s, url, {}, name)
        oldRoot = ET.fromstring(oldCntnt.content)

        for i in oldRoot:
            oldChild = i.getchildren()
            link = oldChild[0].text
            oldAppend(link)

        while True:

            newCntnt = None
            newRoot = None

            time.sleep(timeout)

            t1 = time.time()

            newCntnt = self.getRequ(s, url, {}, name)

            try :
                newRoot = ET.fromstring(newCntnt.content)
                if newCntnt.status_code == 200:
                    passed = True

            except :
                print (('[{}] : lxml error, retrying').format(name))
                passed = False

            if passed == True :

                for i in newRoot:
                    newChild = i.getchildren()
                    link = newChild[0].text

                    if link not in old :
                        try :
                            newChild2 = (newChild[3]).getchildren()
                            title = self.normalizeText(newChild2[1].text)
                            image = newChild2[0].text

                        except :
                            title = self.parseName(link)
                            image = ''

                        if filter == True :

                            if self.filter('{}{}{}'.format(title, image, link)) == True and jsonSelectorOption != None:
                                self.tweetShopifyReply(link, title, image, jsonSelectorOption)
                            else :
                                self.tweetImageData('{}\n{}'.format(title, link), image)


                        else :
                            if self.filter('{}{}{}'.format(title, image, link)) == True  and jsonSelectorOption != None:
                                self.tweetShopifyReply(link, title, image, jsonSelectorOption)
                            else :
                                self.tweetImageData('{}\n{}'.format(title, link), image)

                        old.append(link)

                count +=1
                self.writeUpdate(0, name, len(old), newCntnt.status_code, round((time.time()-t1), 2), count)

            else :
                pass

