import json
import time
import tweepy
import requests
from multiprocessing import Process
from Master import MisilaniousFunctions, SendFunctions, writeFunctions, SocketsMessage


class check(MisilaniousFunctions, SendFunctions, writeFunctions, SocketsMessage):


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

        self.globalList = []

        with open('DoneTasks.out', 'w+') as file:
            file.close()

        with open('ScraperOverFlowSites.py', 'w+') as file :
            file.writelines('## OverFlow Functions Added Recently\n\ndef Server(self):\n\n')
            file.close()

        #Process(target = self.runFunctions, args = ('ScraperOverFlowSites.py', )).start()
        print('Starting run functions')
        #self.runFunctions('ScraperOverFlowSites.py')




    def meshCommerceCheckPID(self, site, pid):

        sizeList = []
        count = 0
        fails = 0
        run = True
        sess = requests.Session()
        name = '{}:{}'.format(site, pid)
        fileName = '{}:{}.out'.format(site, pid)
        self.scrapeUpdateWrite(fileName, 0, pid, 0, 0, 0)

        scrapeUrl = 'https://commerce.mesh.mx/stores/{}/products/{}'.format(site, pid)
        apiKey, userAgent, abreviation = self.getMeshHeaders(site)

        headers = {
            'Host': 'commerce.mesh.mx',
            'Connection': 'keep-alive',
            'X-API-Key': apiKey,
            'Accept': '*/*',
            'X-Debug': '1',
            'Accept-Language': 'en-us',
            'User-Agent': userAgent,
            'Accept-Encoding': 'gzip, deflate',
            'MESH-Commerce-Channel': 'iphone-app'}

        while run == True:

            t1 = time.time()
            time.sleep(1)

            #r = self.simpleGetReq(sess, scrapeUrl, headers, name)
            r = requests.get(scrapeUrl, headers = headers)
            print(r.status_code)
            print(r.content)
            if r != 0:

                if r.status_code != 429:

                    if 'Product could not be found' not in r.text:

                        data = json.loads(r.text)

                        priceData = json.loads(json.dumps(data['price']))
                        isVis = data['isVisible']
                        name = data['name']
                        image = data['mainImage']
                        price = priceData['amount'] + ' Pounds'
                        stockStatus = data['stockStatus']
                        color = data['colourDescription']
                        url = data['URL']
                        addDate = data['dateAdded']
                        maxCart = data['maximumCartQuantity']

                        if data['oneSize'] == False:
                            sizeData = json.loads(json.dumps(data['options']))
                            for i in sizeData:
                                d = json.loads(json.dumps(sizeData[i]))
                                sku = d['SKU']
                                ss = d['stockStatus']
                                clr = d['colourDescription']
                                sz = d['size']
                                sizeList.append('%s :\n\tStock status : %s\n\tSKU : %s\n\tColor : %s\n' % (i, ss, sku, clr))
                        else:
                            pass

                        FinalText = 'Name : {}\n\nPID : {}\n\nURL : {}\n\nDate added : {}\n\nFound at {}\n\nPrice : {}\n\nColor : {}\n\nImage URL : {}\n\nIs visable : {}\n\nIs in stock : {}\n\nMax cart quanity : {}\n\n{}'.format(name, pid, url, addDate, self.t(), price, color, image, isVis, stockStatus, maxCart,'\n'.join(sizeList))

                        self.writeTxt(fileName, FinalText)
                        haste = self.makeHaste(FinalText)
                        self.tweetImageData('{}\n{}\n{}'.format(name, url, haste),'http://i1.adis.ws/i/jpl/{}_{}_a?w=950&h=750'.format(abreviation, pid))
                        print('{} - product loaded under pid {}'.format(site, pid))
                        run = False

                    else:
                        count += 1
                        self.scrapeUpdateWrite(fileName, 0, pid, count, time.time() - t1, fails)
                else:
                    print('[{}] : 429 error, site - {}, pid - {}, meshLoad'.format(self.t(), site, pid))
                    fails += 1
                    self.scrapeUpdateWrite(fileName, 0, pid, count, time.time() - t1, fails)

            else:
                fails += 1
                self.scrapeUpdateWrite(fileName, 0, pid, count, time.time() - t1, fails)

        with open("DoneTasks.out", 'a') as file:
            file.append("{} - {} restock\n".format(site, pid))
            file.close()


    def barneyPIDscrape(self, pid ):

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


        count = 0
        fails = 0
        run = True
        stockList = []
        sizeIDlist = []
        sess = requests.Session()
        name  = 'Barneys-update-{}'.format(pid)
        fileName = 'Barneys-update-{}.out'.format(pid)
        scrapeUrl = 'https://www.barneys.com/rest/model/barneys/commerce/catalog/BNYProductDetailDisplayActor/getProductDetailsPageInfo?productId={}'.format(pid)

        while run == True :

            t1 = time.time()
            time.sleep(2)

            r = self.simpleGetReq(sess, scrapeUrl, headers, name)

            if (r != 0) :

                if (r.status_code == 200) and ('Please verify if the product id is valid' not in r.text):
                    data = json.loads(r.text)

                    inventoryData = json.loads(json.dumps(data['inventoryDetails']))
                    skuInventoryData = json.loads(json.dumps(inventoryData['skuInventoryStatus']))

                    prodData = json.loads(json.dumps(data['productDetails']))
                    prodData2 = json.loads(json.dumps(prodData[0]))
                    atrData = json.loads(json.dumps(prodData2['attributes']))

                    category = str(atrData['parentCategory.displayName'][0])
                    skuData = json.loads(json.dumps(skuInventoryData['skuInventoryATP']))
                    images = atrData['product.auxImageURLS']
                    creationDate = str(time.ctime(int(str(atrData['product.creationDate'][0]))))
                    dateAvalable = str(time.ctime(int(str(atrData['product.dateAvailable'][0]))))
                    designer = atrData["product.designer"][0]
                    name = atrData['product.displayName'][0]
                    price = atrData['product.maxPrice'][0]
                    url = 'http://www.barneys.com/' + str(atrData['product.productDetailPageUrl'][0])
                    respID = atrData['product.repositoryId'][0]
                    sizes = atrData['sku.realSize']

                    string = ('Name : {}\nBrand : {}\nCategory : {}\nPrice : ${}0\nCreated at {}\nAvalable at {}\nURL : {}\nRespitory ID : {}\n\n'.format(name, designer, category, price, creationDate, dateAvalable, url, respID))
                    string += 'Images :\n'

                    for i in images :
                        string += ('\t' + i[16:] + '\n')

                    string += '\n'

                    for sizeID, stock in skuData.items():
                        sizeIDlist.append(sizeID)
                        stockList.append(stock)

                    string += 'Sizes : \n'
                    for sz, szID, stk in zip(sizes, sizeIDlist, stockList) :
                        string += ('\tSize : {} - PID : {} - Stock : {}\n '.format(sz, szID, stk))

                    self.writeTxt(fileName, string)
                    self.tweetImageData('{}\n{}\n{}'.format(name, url, self.makeHaste(string)), images[0][16:])
                    run = False


                else :
                    #self.scrapeUpdateWrite(fileName, 0, pid, count, time.time()-t1, fails)
                    if r.status_code != 200 :
                        print ('{} {} error with barneys pid {}'.format(self.t(), r.status_code, pid))
                        fails += 1
                    else :
                        count += 1
                    self.scrapeUpdateWrite(fileName, 0, pid, count, time.time()-t1, fails)

            else :
                fails += 1
                self.scrapeUpdateWrite(fileName, 0, pid, count, time.time()-t1, fails)

        with open("DoneTasks.out", 'a') as file:
            file.append("BNY - {} restock\n".format( pid))
            file.close()

check().meshCommerceCheckPID('footpatrol', '060980')











































