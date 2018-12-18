import time
import tweepy, requests
import json
from threading import  Thread
from multiprocessing import Process
from Master import MisilaniousFunctions, SendFunctions, writeFunctions, SocketsMessage
from StockPrice import StockPriceMonitor
 
 
class userInput(StockPriceMonitor):

    def __init__(self):

        self.keyList = [ \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE','TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE'], \
            ['TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE', 'TWITTER API KEY HERE']]

        authList = self.keyList[0]

        auth = tweepy.OAuthHandler(authList[0], authList[1])
        auth.set_access_token(authList[2], authList[3])

        self.api = tweepy.API(auth)

        self.runningFunctions = []

        with open('RunningFunctions.out', 'r') as file:
            for i in file.readlines():
                self.runningFunctions.append(i.replace('\n', ''))
            file.close()

        self.keyIndex = 0
        self.startTime = time.time()
        self.restockMonitorIP = '173.199.117.98'
        self.scraperMonitorIP = '173.199.117.98'
        self.sneakerStockMonitorIP = '173.199.117.98'



    def twitterDmlisten(self):

        self.dmsRead = 0
        self.dmsAdded = 0
        self.restockSendFunct = []
        self.scrapeSendFunct = []
        self.stockSendFunct = []
        baseDM = self.api.direct_messages()[0].id

        self.writeTxt('DM-listen.out', '{}\n\nTwitter DM Listener\n\nStart time : {}\n\nTime Elapsed : Null\n\nDMs read : 0\n\nDms added : 0'.format(time.time(), self.t()))

        while True :

            time.sleep(15)

            DMlist = self.tweetGetDMs(baseDM)

            if len(DMlist) != 0:
                baseDM = DMlist[0].id

            self.dmsRead += len(DMlist)

            self.restockSendFunct[:] = []
            self.scrapeSendFunct[:] = []
            self.stockSendFunct[:] = []

            for i in DMlist:

                formatOK = False

                try :
                    DMtext = str(i.text).replace('\n', '')
                    if DMtext.count('*') == 2 and ' ' not in DMtext:
                        formatOK = True
                except :
                    formatOK = False

                if formatOK == True:

                    if any(kw in DMtext for kw in ['*fpLoad*', '*szLoad*', '*jdLoad*', '*tsLoad*']):

                        if '*fpLoad*' in DMtext:
                            site = 'footpatrol'
                            abrev = 'fp'
                            try :
                                pid = DMtext.replace('*fpLoad*', '')
                                int(pid)
                                passed = True
                            except :
                                passed = False

                        elif '*szLoad*' in DMtext:
                            site = 'size'
                            abrev = 'sz'
                            try :
                                pid = DMtext.replace('*szLoad*', '')
                                int(pid)
                                passed = True
                            except :
                                passed = False

                        elif '*jdLoad*' in DMtext:
                            site = 'jdsports'
                            abrev = 'jd'
                            try :
                                pid = DMtext.replace('*jdLoad*', '')
                                int(pid)
                                passed = True
                            except :
                                passed = False

                        elif '*tsLoad*' in DMtext:
                            site = 'tessuti'
                            abrev = 'ts'
                            try :
                                pid = DMtext.replace('*tsLoad*', '')
                                int(pid)
                                passed = True
                            except :
                                passed = False
                        else :
                            passed = False

                        ISurl, ISname = self.meshCommerceIsLoaded(site, pid)

                        if ISurl == False and len(pid) == 6 and passed == True :

                            dataList = ['meshCommerceCheckPID', site, pid]
                            dataString = self.returnDataString(dataList)

                            if dataString not in self.runningFunctions:
                                self.runningFunctions.append(dataString)
                                self.scrapeSendFunct.append(dataList)
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! Xeno Monitor is now monitoring {} on www.{}.co.uk for updates.".format(pid, site))
                            else :
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! Xeno Monitor is already monitoring {} on www.{}.co.uk".format(pid, site))

                        else :
                            if ISurl != False :
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However {} is already loaded on www.{}.co.uk ! The url is {} . Did you mean to check for a restock? The correct formating for a restock would be \n\n*{}Restock*\n{}".format(ISname, site, ISurl, abrev, pid))
                            elif len(str(pid)) != 6:
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However that pid is incorrect, PIDs should be 6 digits long check the documentation here INSERT DOCS")
                            else :
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However that request is formated incorrectly, check the docs here INSERT DOCS")

                    elif any(kw in DMtext for kw in ['*fpRestock*', '*szRestock*', '*jdRestock*', '*tsRestock*']):

                        if '*fpRestock*' in DMtext:
                            site = 'footpatrol'
                            abrev = 'fp'
                            pid = DMtext.replace('*fpRestock*', '')


                        elif '*szRestock*' in DMtext:
                            site = 'size'
                            abrev = 'sz'
                            pid = DMtext.replace('*szRestock*', '')

                        elif '*jdRestock*' in DMtext:
                            site = 'jdsports'
                            abrev = 'jd'
                            pid = DMtext.replace('*jdRestock*', '')

                        elif '*tsRestock*' in DMtext:
                            site = 'tessuti'
                            abrev = 'te'
                            pid = DMtext.replace('*tsRestock*', '')

                        else :
                            passed = False

                        try :
                            int(pid)
                            passed = True
                        except :
                            passed = False

                        ISurl, ISname = self.meshCommerceIsLoaded(site, pid)

                        if ISurl != False and len(pid) == 6 and passed == True:

                            dataList = ['meshCommerceRestock', site, pid]
                            dataString = self.returnDataString(dataList)

                            if dataString not in self.runningFunctions:
                                self.runningFunctions.append(dataString)
                                self.restockSendFunct.append(dataList)
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! Xeno Monitor is now monitoring {} for restocks on www.{}.co.uk.".format(ISname, site))
                            else :
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! Xeno Monitor is already monitoring {} on www.{}.co.uk.".format(ISname, site))

                        else :
                            if ISurl == False :
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However {} is not loaded on {}! Did you mean to check for a update? If you did the correct format is \n\n*{}Restock*\n{}".format(pid, site, abrev, pid))
                            elif len(str(pid)) != 6:
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However that pid is invalid, PIDs should be 6 digits long check the documentation here INSERT DOCS")
                            else :
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However {} is not formated correctly, check the docs here INSERT DOCS")

                    elif '*bnyLoad*' in DMtext:

                        try :
                            pid = DMtext.replace('*bnyLoad*', '')
                            int(pid)
                            passed = True
                        except :
                            passed = False

                        if passed == True and len(pid) == 9 :

                            ISurl, ISname = self.bnyIsLoaded(pid)

                            if ISurl == False :

                                dataList = ['barneyPIDscrape', pid]
                                dataString = self.returnDataString(dataList)

                                if dataString not in self.runningFunctions:
                                    self.runningFunctions.append(dataString)
                                    self.scrapeSendFunct.append(dataList)
                                    self.tweetDM(i.sender.id, "Thank you for the recommendation! Xeno Monitor is now monitoring {} on www.barneys.com for updates.".format(pid))
                                else :
                                    self.tweetDM(i.sender.id, "Thank you for the recommendation! Xeno Monitor is already monitoring {} www.barneys.com for updates.".format(pid))
                            else :
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However {} is already loaded on www.barneys.com, the url is {}. Did you mean to check for a restock? if so the correct formating would be \n\n*bnyRestock*\n{}".format(ISname, ISurl, pid))
                        else :
                            if passed == False :
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However {} is not formated correctly! check the documentation here DOCS HERE".format(pid))
                            elif len(str(pid)) != 9:
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However that pid is incorrect, PIDs for www.barneys.com should be 9 digits long check the documentation here INSERT DOCS")

                    elif '*bnyRestock*' in DMtext:

                        try :
                            pid = DMtext.replace('*bnyRestock*', '')
                            int(pid)
                            passed = True
                        except :
                            passed = False

                        if passed == True and len(pid) == 9 :

                            ISurl, ISname = self.bnyIsLoaded(pid)

                            if isUrl != False:

                                dataList = ['barneyPIDrestock', pid]
                                dataString = self.returnDataString(dataList)

                                if dataString not in self.runningFunctions:
                                    self.runningFunctions.append(dataString)
                                    self.restockSendFunct.append(dataList)
                                    self.tweetDM(i.sender.id, "Thank you for the recommendation! Xeno Monitor is now monitoring {} on www.barneys.com for restocks.".format(ISname))
                                else :
                                    self.tweetDM(i.sender.id, "Thank you for the recommendation! Xeno Monitor is already monitoring {} on www.barneys.com for restocks.".format(ISname))
                            else :
                                self.tweetDM(i.sender.id, "Thankyou for the recomendation! However {} is not loaded on www.barneys.com, did you mean to check for updates? If so the correct format would be \n\n*bnyLoad*\n{}".format(pid, pid))

                        else :
                            if passed == False :
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However {} is not formated correctly! check the documentation here DOCS HERE".format(pid))
                            elif len(str(pid)) != 9:
                                self.tweetDM(i.sender.id, "Thank you for the recommendation! However that pid is incorrect, PIDs for www.barneys.com should be 9 digits long check the documentation here INSERT DOCS")

                    elif '*shopRestock*' in DMtext:
                        url = DMtext.replace('*codeChange*', '') + '.json'

                        isUrl = self.isUrl(url)

                        if isUrl == True:

                            if self.isShop(url) == True:

                                if self.isShopStock(url) == True:

                                    dataList = ['shopRestock', url, 1.5, self.parseName(url)]
                                    dataString = self.returnDataString(dataList)

                                    if dataString not in self.runningFunctions:
                                        self.runningFunctions.append(dataString)
                                        self.restockSendFunct.append(['shopRestock', url, 1.5, self.parseName(url)])
                                        self.tweetDM(i.sender.id,
                                                     "Thank you for the recommendation! Xeno Monitor is now checking for restocks on {}.".format(
                                                         url))

                                    else:
                                        self.tweetDM(i.sender.id,
                                                     "Thank you for the recommendation! However Xeno Monitor is already checking for restocks on {}.".format(
                                                         url))

                                else:
                                    self.tweetDM(i.sender.id,
                                                 "Thank you for the recommendation! However even though {} is a shopify site, *shopRestock* does not work on that site, there are other functions used to monitor page content, you can find those here INSERT DOCS HERE.".format(
                                                     url))

                            else:
                                self.tweetDM(i.sender.id,
                                             "Thank you for the recomendation! However that is not a shopify site, there are other options for monitoring non shopify sites, check the docs here INSERT DOCS")
                        else:
                            self.tweetDM(i.sender.id,
                                         "Thank you for the recommendation! However that does not apear to be a url, urls should be in the form of http://site.domaine.com, make sure that all you formating is correct here INSERT DOCS")

                    elif '*codeChange*' in DMtext:
                        url = DMtext.replace('*codeChange*', '')

                        isUrl = self.isUrl(url)

                        if isUrl == True:

                            r = self.simpleGetReq(requests.Session(), url, {}, 'codeChange test')

                            if r.status_code not in [403, 430, 0]:

                                if self.isMesh(url) == False:
                                    dataList = ['codeChange', url, 'image', {}, 1, self.parseName(url)]
                                    dataString = self.returnDataString(dataList)

                                    if dataString not in self.runningFunctions:
                                        self.runningFunctions.append(dataString)
                                        self.restockSendFunct.append(dataList)
                                        self.tweetDM(i.sender.id,
                                                     "Thank you for the recommendation! Xeno Monitor is now checking for status code updates on {}".format(
                                                         url))
                                    else:
                                        self.tweetDM(i.sender.id,
                                                     "Thank you for the recommendation! However Xeno Monitor is already checking for status code updates on {}".format(
                                                         url))

                                else:
                                    self.tweetDM(i.sender.id,
                                                 "Thank you for the recomendation! However that is a mesh commerce site, Xeno Monitor has functions specially developed for mesh commerce sites, check the docs here DOCS HERE ")

                            else:
                                self.tellegramMessage(
                                    'Error adding website, {} error, {}'.format(r.status_code, DMtext))
                                self.tweetDM(i.sender.id,
                                             "Thank you for the recommendation! However there apears to be an error, we're banned from that website! A report has been filed and we are working to fix it ASAP, if you have any more questions message @SoleWingSneaks")

                        else:
                            self.tweetDM(i.sender.id,
                                         "Thank you for the recommendation! However that request is not properly formated, urls should be in the form of http://site.domaine.com, make sure that all you formating is correct here INSERT DOCS")

                    elif '*textChange*' in DMtext:
                        url = DMtext.replace('*textChange*', '')

                        isUrl = self.isUrl(url)

                        if isUrl == True:
                            if r.status_code not in [403, 430]:

                                if self.isMesh(url) == False:

                                    dataList = ['textRestock', url, 'image', 'selector', {}, 1, self.parseName(url)]
                                    dataString = self.returnDataString(dataList)

                                    if dataString not in self.runningFunctions:
                                        self.runningFunctions.append(dataString)
                                        self.restockSendFunct.append(dataList)
                                        self.tweetDM(i.sender.id,
                                                     "Thank you for the recommendation! Xeno Monitor is now checking for web page changes in {}.".format(
                                                         url))
                                    else:
                                        self.tweetDM(i.sender.id,
                                                     "Thank you for the recommendation! However Xeno Monitor is already checking for web page changes in {}.".format(
                                                         url))

                                else:
                                    self.tweetDM(i.sender.id,
                                                 "Thank you for the recomendation! However that is a mesh commerce site, Xeno Monitor has functions specially developed for mesh commerce sites, check the docs here DOCS HERE ")

                            else:
                                self.tellegramMessage('Error adding website {}'.format(DMtext))
                                self.tweetDM(i.sender.id,
                                             "Thank you for the recommendation! However there apears to be an error, we're banned from that website! A report has been filed and we are working to fix it ASAP, if you have any more questions message @SoleWingSneaks")

                        else:
                            self.tweetDM(i.sender.id,
                                         "Thank you for the recommendation! However that does not apear to be a url, urls should be in the form of http://site.domaine.com, make sure that all you formating is correct here INSERT DOCS")

                    elif '*pageChange*' in DMtext:
                        url = DMtext.replace('*pageChange*', '')

                        isUrl = self.isUrl(url)

                        if isUrl == True:
                            if r.status_code not in [403, 430]:

                                if self.isMesh(url) == False:

                                    dataList = ['pageContentChange', url, {}, 1, self.parseName(url)]
                                    dataString = self.returnDataString(dataList)

                                    if dataString not in self.runningFunctions:
                                        self.runningFunctions.append(dataString)
                                        self.restockSendFunct.append(dataList)
                                        self.tweetDM(i.sender.id,
                                                     "Thank you for the recommendation! Xeno Monitor is now checking for web page changes in {}.".format(
                                                         url))
                                    else:
                                        self.tweetDM(i.sender.id,
                                                     "Thank you for the recommendation! However Xeno Monitor is already checking for web page changes in {}.".format(
                                                         url))

                                else:
                                    self.tweetDM(i.sender.id,
                                                 "Thank you for the recomendation! However that is a mesh commerce site, Xeno Monitor has functions specially developed for mesh commerce sites, check the docs here DOCS HERE ")

                            else:
                                self.tellegramMessage('Error adding website {}'.format(DMtext))
                                self.tweetDM(i.sender.id,
                                             "Thank you for the recommendation! However there apears to be an error, we're banned from that website! A report has been filed and we are working to fix it ASAP, if you have any more questions message @SoleWingSneaks")

                        else:
                            self.tweetDM(i.sender.id,
                                         "Thank you for the recommendation! However that does not apear to be a url, urls should be in the form of http://site.domaine.com, make sure that all you formating is correct here INSERT DOCS")

                    elif '*sneakerStock*' in DMtext:

                        pkg = self.getStockXPackage(DMtext.replace('*sneakerStock*', '').replace('@', ''))

                        if pkg != []:

                            dataList = ['stockX', pkg[0], pkg[1]]
                            dataString = self.returnDataString(dataList)

                            if dataString not in self.runningFunctions:
                                self.runningFunctions.append(dataString)
                                self.stockSendFunct.append(dataList)
                                self.tweetDM(i.sender.id, "Thank you for the recomendation! Xeno Monitor is now checking for changes in the price of {}".format(pkg[1]))

                            else :
                                self.tweetDM(i.sender.id, "Thank you for the recomendation! However Xeno Monitor is already monitoring for price changes in {}".format(pkg[1]))
                                #self.stockSendFunct.append(['getSneakerStock', str(i.sender.id)])
                        else :
                            self.tweetDM(i.sender.id, "Thank you for the recomendation! However that request was not formated correctly, check the docs here INSERT DOCS to make sure it was formated correctly")
              
                    #elif '*getSneakerStock*' in DMtext:
                    #    dataList = ['getSneakerStock', str(i.sender.id)]
                    #    self.stockSendFunct.append(dataList)
          

                else :
                    self.tweetDM(i.sender.id, "Thank you for the recommendation! However there is an error with your formating and we can not monitor that, check the documentation here DOCS HERE and try again")

            self.dmsAdded += len(self.stockSendFunct) + len(self.restockSendFunct) + len(self.scrapeSendFunct)
            
            if self.stockSendFunct != []:
                self.socketSend(self.sneakerStockMonitorIP , self.stockSendFunct)

            if self.restockSendFunct != []:
                self.socketSend(self.restockMonitorIP, self.restockSendFunct)

            if self.scrapeSendFunct != []:
                self.socketSend(self.scraperMonitorIP, self.scrapeSendFunct)

            self.writeDmListen(0)


            for i in [self.stockSendFunct, self.scrapeSendFunct, self.restockSendFunct] :
                for n in i:
                    with open('RunningFunctions.out', 'a') as file:
                        text = self.returnDataString(n) + '\n'
                        file.append(text)

userInput().twitterDmlisten()













