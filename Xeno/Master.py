import os
import json
import time
import shutil
import socket
import select
import random
import tweepy
import smtplib
import requests
import datetime
import unicodedata
from io import StringIO
from lxml.html import parse
from threading import  Thread
from multiprocessing import Process
import xml.etree.ElementTree as ET

try :
    from pytz import timezone
except :
    pass
try :
    import urllib.request
except :
    import urllib


class RequestFunctions:

    def getSeleniumMesh(self, driver):

        n = 0

        driver.refresh()

        while True:

            if n >= 500:
                print("{} Error with footpatrol, sleeping.......")
                time.sleep(99999999999999999999999)
            elif 'Latest Footwear' in driver.page_source:
                break
            else:
                time.sleep(1)
                n += 1

    def simpleGetReq(self, sess, url, headers, name):
        passed = False
        # fileName = '{}.out'.format(name.replace(' ', '-'))
        trys = 0

        while passed == False and trys <= 5:

            try:
                r = sess.get(url, headers=headers, allow_redirects=False)
                passed = True
            except:
                trys += 1
                if trys == 5:
                    print('{} - Failed to make connection to {}'.format(self.t(), url))
                    # self.appendTxt(fileName,'{} failed to get {}\n\n'.format(self.t(), url))
                    r = 0
        return r

    def simplePostReq(self, session, url, data, headers, name):
        passed = False
        # fileName = '{}.out'.format(name.replace(' ', '-'))
        trys = 0

        while passed == False and trys <= 5:

            try:
                r = session.post(url, data=data, headers=headers)
                passed = True
            except:
                trys += 1
                if trys == 5:
                    print('{} - Failed to make connection to {}'.format(self.t(), url))
                    # self.appendTxt(fileName,'{} failed to get {}\n\n'.format(self.t(), url))
                    r = 0
        return r

    def getRequ(self, sess, url, headers, name):

        passVar = False
        fileName = '{}.out'.format(name.replace(' ', '-'))

        while passVar == False:

            try:
                r = sess.get(url, headers=headers, verify=False)
                sCode = r.status_code
            except:
                self.writeReqError(fileName, 0, 0)
                sCode = 0

            if sCode == 200:
                passVar = True

            elif sCode == 430:
                self.writeReqError(fileName, 0, 430)
                time.sleep(30)
                self.getRequ(sess, url, headers, name)

            elif sCode in [404, 403]:
                self.writeReqError(fileName, 0, sCode)
                self.tellegramMessage('{} - {} error, sleeping for 2 minutes'.format(name, sCode))
                time.sleep(120)
                self.getRequ(sess, url, headers, name)

            else:
                self.writeReqError(fileName, 0, sCode)

        return r

class SendFunctions:

    def tellegramMessage(self, txt):
        requests.get("https://api.telegram.org/bot242856518:AAG_2HrAug_U1sbIOEukJGngqLbAz3qfpBk/sendMessage?chat_id=-1001076025110&text=%s" % txt)

    def textMessage(self, txt):
        requests.get("https://api.telegram.org/bot242856518:AAG_2HrAug_U1sbIOEukJGngqLbAz3qfpBk/sendMessage?chat_id=-1001076025110&text=%s" % txt)
        
        '''
        requests.get("https://api.telegram.org/bot242856518:AAG_2HrAug_U1sbIOEukJGngqLbAz3qfpBk/sendMessage?chat_id=-1001070993194&text=%s" % txt)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("Leelthefantabulous@gmail.com", "Leelmore$$")
        server.sendmail("Leelthefantabulous@gmail.com", "3306031362@vtext.com", txt)
        server.quit()
        '''

    def cycle(self):
        self.keyIndex = (0 if self.keyIndex == (len(self.keyList) - 1) else (self.keyIndex + 1))
        authList = self.keyList[self.keyIndex]
        auth = tweepy.OAuthHandler(authList[0], authList[1])
        auth.set_access_token(authList[2], authList[3])
        self.api = tweepy.API(auth)

    def tweetRegular(self, text):
        try:
            self.api.update_status(text)
        except:
            try:
                self.cycle()
                self.api.update_status(text)
            except Exception as e :
                self.writeTWE(e)
                self.tellegramMessage('Tweet error - {}'.format(text))
                print(('[ {} ] : Error tweeting "{}"').format(str(time.strftime('%H:%M:%S', time.localtime())), str(text)))

    def tweetImageData(self, text, image):
        try :
            randStr = self.getRandString()
            shutil.copyfileobj( requests.get(image, stream=True).raw,  open(randStr, 'wb') )
        except :
            pass

        try:
            t = self.api.update_with_media(randStr, status=text)
            os.remove(randStr)

        except:
            try:
                t = self.api.update_status(text)
            except:
                try:
                    self.cycle()
                    t = self.api.update_status(text)
                except Exception as e:
                    #self.writeTWE(e)
                    #self.tellegramMessage('Tweet error - {}'.format(text))
                    t = False
                    print(('[ {} ] : Error tweeting "{}"').format(self.t(), str(text)))
        return t

    def tweetDM(self, user_id, text):
        try:
            self.api.send_direct_message(user_id = user_id, text = text)
        except:
            try:
                self.cycle()
                self.api.send_direct_message(user_id = user_id, text = text)
            except Exception as e:
                self.writeTWE(e)
                self.tellegramMessage('Tweet DM error - %s' % text)
                print(('[ {} ] : Error tweeting "{}"').format(str(time.strftime('%H:%M:%S', time.localtime())), str(text)))
                time.sleep(5)

    def tweetGetDMs(self, since_ID):
        try :
            DMs = self.api.direct_messages(since_id = since_ID, count = 100)
        except:
            try:
                self.cycle()
                DMs = self.api.direct_messages(since_id = since_ID, count = 100)
            except Exception as e :
                self.writeTWE(e)
                self.tellegramMessage('Error retreaving DMs')
                DMs = []
        return DMs

class writeFunctions:

    def joinListList(self, ListList):
        returnList = []
        for i in ListList:
            returnList.append('{} : '.format(i[0], ' - '.join(i[1:])))
        return '\t{}'.format('\n\t'.format(returnList))

    def getTimeElapsed(self, fileName):

        with open(fileName, 'r') as file :
            strtTime = float(file.readlines()[0])
            file.close()

        timeElapsed = time.time() - strtTime
        weeks = (0 if timeElapsed/604800 < 1 else int(timeElapsed/604800))
        timeElapsed -= (weeks * 604800)
        days = (0 if timeElapsed/86400 < 1 else int(timeElapsed/86400))
        timeElapsed -= (days*86400)
        hours = (0 if timeElapsed/3600 < 1 else int(timeElapsed/3600))
        timeElapsed -= (hours*3600)
        minutes = (0 if timeElapsed/60 < 1 else int(timeElapsed/60))
        timeElapsed -= (minutes*60)
        seconds = int(timeElapsed)
        return 'Total run time - [{} Week(s), {} Day(s), {} Hour(s), {} Minute(s), {} Second(s)]'.format(weeks, days, hours, minutes, seconds)

    def appendTxt(self, fileName, text):
        with open(fileName, 'a') as file :
            file.write('{}\n'.format(text) )
            file.close()

    def writeTxt(self, fileName, text):
        with open(fileName, 'w') as file :
            file.write(text + '\n')
            file.close()

    def writeFile(self, name):
        fileName = '{}.out'.format(name.replace(' ', '-'))
        with open(fileName, 'w+') as file :
            file.write('{}\n\n{}\n\nProccess started at {}\n\nTime Elapsed : Null\n\nMost Recent failed get - [NULL]\n\tFail Count - 0\n\tStatus code - [NULL]\n\nMost recent succsesfull check - [NULL]\n\tSuccses count - 0\n\tLink count - [NULL]\n\tStatus code - [NULL]\n\tCheck time - [NULL]'.format(time.time(), name, self.t()))
            file.close()

    def writeTWE(self, e):    
        with open('TwitterErrorLog.out', 'w') as file :
            data = file.readlines()
            data.append('\n{}\n'.format(e))
            file.writelines(data)
            file.close()

    def writeDmListen(self, recurRate):

        try :
            with open('DM-listen.out', 'r') as file :
                data = file.readlines()
                file.close()

            data[4+2] = '{}\n'.format(self.getTimeElapsed("DM-listen.out"))
            data[6+2] = 'DMs read : {}\n'.format(self.dmsRead)
            data[8+2] = 'DMs added : {}\n'.format(self.dmsAdded)

            with open('DM-listen.out', 'w') as file:
                file.writelines(data)
                file.close()

            if self.stockSendFunct != [] or self.restockSendFunct != [] or self.scrapeSendFunct != []:
                    stockSendData = (self.joinListList(self.stockSendFunct) if self.stockSendFunct != [] else '')
                    restockSendData = (self.joinListList(self.restockSendFunct) if self.restockSendFunct != [] else '')
                    scrapeSendData = (self.joinListList(self.scrapeSendFunct) if self.scrapeSendFunct != [] else '')

                    if (len(stockSendData) + len(restockSendData) + len(scrapeSendData)) > 0:
                        masterMessage = '\n{}\n'.format(self.t())

                        for i in [scrapeSendData, restockSendData, stockSendData]:
                            masterMessage += '\t{}\n'.format(i)

                        with open('DM-listen.out', 'a') as file :
                            file.writelines(masterMessage)
                            file.close()

        except Exception as e :
            if recurRate == 5:
                print (e)
                print ('{} Error writing DM-listen.out, dms read - {}, dms added - {}, stock funct - {}, restock funct - {}, scrape funct {}'.format(self.t(), self.dmsRead, self.dmsAdded, self.stockSendFunct, self.restockSendFunct,  self.scrapeSendFunct ))
            else :
                recurRate += 1
                print ('{} error writing DM-listener.out, retrying, try number - {}'.format(self.t(), recurRate))
                self.writeDmListen(recurRate)

    def writePythonFile(self, fileName, text):
        with open(fileName, 'a') as file :
            file.writelines('\t{}\n'.format(text))
            file.close()

    def writeUpdate(self, recurRate, name, linkCount, sCode, cTime, count):

        fileName = '{}.out'.format(name.replace(' ', '-'))

        try :
            with open(fileName, 'r') as file :
                data = file.readlines()
                data[4+2] = '{}\n'.format(self.getTimeElapsed(fileName))
                data[10+2] = 'Most recent succsesfull check - [{}]\n'.format(self.t())
                data[11+2] = '\tSuccses count - {}\n'.format(count)
                data[12+2] = '\tLink Count - [{}]\n'.format(linkCount)
                data[13+2] = '\tStatus Code - [{}]\n'.format(sCode)
                data[14+2] = '\tCheck Time - [{}]\n'.format(cTime)
                file.close()

            with open(fileName, 'w') as file:
                file.writelines( data )
                file.close()

        except Exception as e :
            recurRate += 1
            if recurRate == 5:
                print (e)
                print ("[{}] : Could not write linkCount- {}, sCode - {}, cTime - {}, count - {}, to {} recursion limit exceded".format(self.t(),linkCount, sCode, cTime, count, fileName))
            else :
                print ("{} error writing {}, retrying, try number {}".format(self.t(), recurRate))
                self.writeUpdate(recurRate, name, linkCount, sCode, cTime, count)
   
    def writeStockX(self, fileName, trys, checks, changes):
            
            try :
                with open(fileName, 'r') as file :
                    data = file.readlines()
                    file.close()

                
                data[8] = '{}\n'.format(self.getTimeElapsed(fileName))
                data[10] = 'Checks {}\n'.format(checks)

                with open(fileName, 'w+') as file :
                    file.writelines(data)
                    file.close()

                with open(fileName, 'a') as file :
                    file.writelines(changes)
                    file.close()

            except Exception as e :
                if trys == 5:
                    print (e)
                    print ('[{}] : Failed to write {}, checks - {}, changes - {}'.format(self.t(), fileName, checks, changes))
                else :
                    trys+=1
                    print ('[{}] : Failed to write {}, trys - {}, retrying....'.format(self.t(), fileName, trys))
       
    def writeScode(self, name, recurRate, count, fails, codeHist):

        fileName = '{}.out'.format(name.replace(' ', '-'))

        try :
            with open(fileName, 'r') as file :
                data = file.readlines()
                file.close()

            data[4+2] = '{}\n'.format(self.getTimeElapsed(fileName))
            data[6+2] = 'Checks : {}\n'.format(count)
            data[8+2] = 'Fails : {}\n'.format(fails)
            data[10+2] = 'Code History : [{}]\n'.format('->'.join(codeHist))

            with open(fileName, 'w') as file:
                file.writelines(data)
                file.close()
        except Exception as e :
            recurRate += 1
            if recurRate == 5:
                print (e)
                print ('[{}] : Failed to write name - {}, count - {}, fails - {}, code hist - {} '.format(self.t(), name, count, fails, codeHist))
            else:
                print ('[{}] : Failed to write {}, retrying, try number {}'.format(self.t(), fileName, recurRate))
                self.writeScode(name, recurRate, count, fails, codeHist)

    def writePageChange(self, name, recurRate, checks, fails, update):

        fileName = '{}.out'.format(name.replace(' ', '-'))

        try :
            with open(fileName, 'r') as file :
                data = file.readlines()
                file.close()

            data[4+2] = '{}\n'.format(self.getTimeElapsed(fileName))
            data[6+2] = 'Checks : {}\n'.format(checks)
            data[8+2] = 'Fails : {}\n'.format(fails)

            with open(fileName, 'w') as file :
                file.writelines(data)
                file.close()

            if update != False :
                with open(fileName, 'a') as file :
                    file.writelines(update)
                    file.close()

        except Exception as e :
            recurRate += 1
            if recurRate >= 5:
                print (e)
                print ('Error writing {} at {}, checks {}, fails {}, update {}'.format(fileName, self.t(), checks, fails, update))
            else :
                print ('Error writing {}, atempt {}'.format(fileName, recurRate))
                self.writePageChange(fileName, recurRate, checks, fails, update)

    def writeReqError(self, fileName, recurRate, code):

        try :
            with open(fileName, 'r') as file :
                data = file.readlines()
                data[4+2] = '{}\n'.format(self.getTimeElapsed(fileName))
                data[6+2] = 'Most Recent failed get - [{}]\n'.format(self.t())
                for i in range(0, len(data[7+2])):
                    if data[7+2][i] == '-':
                        fails = int(data[7+2][i+1:]) + 1
                data[7+2] = '\tFail count - {}\n'.format(fails)
                data[8+2] = '\tStatus code - [{}]\n'.format(code)
                file.close()

            with open(fileName, 'w') as file :
                file.writelines(data)
                file.close()

        except Exception as e :
            recurRate += 1
            if recurRate == 5:
                print (e)
                print ("[{}] : Could not write status code - {} to {} recursion limit exceded".format(self.t(), code, fileName))
            else :
                print ("[{}] : Error writing {}, retrying, try number {}".format(self.t(), fileName, recurRate))
                self.writeReqError(fileName, recurRate, code)

    def writeShopifyRestock(self, name, recurRate, count, fails, last430, restocks):

        fileName = '{}.out'.format(name.replace(' ', '-'))

        try :
            with open(fileName,'r') as file :
                data = file.readlines()
                file.close()

            data[4+2] = '{}\n'.format(self.getTimeElapsed(fileName))
            data[6+2] = 'Checks : {}\n'.format(count)
            data[8+2] = 'Fails : {}\n'.format(fails)
            data[10+2] = 'Last 430 : {}\n'.format(last430)

            with open(fileName, 'w') as file :
                file.writelines(data)
                file.close()

            if restocks != False :
                with open(fileName, 'a') as file :
                    file.writelines(restocks)
                    file.close()
        except Exception as e :
            recurRate += 1
            if recurRate > 5:
                print (e)
                print ("Failed to write {} at {}, count - {}, fails - {}, last 430 - {}, restocks - {}".format(fileName, self.t(), count, fails, last430, restocks))
            else:
                print ('Failed to write {}, atmept number {}'.format(fileName, recurRate))
                self.writeShopifyRestock(fileName, recurRate, count, fails, last430, restocks)

    def scrapeImageWrite(self, fileName, recurRate, start, stop, checks, checkTime, fails, failList):

        if checks == 0:
            with open(fileName, 'w+') as file :
                file.writelines('{}\n\n{}-{}\n\nStart time : [{}]\n\nTime elapsed : [0]\n\nTotal number of checks : 0\n\nLast check time : 0\n\nFailed gets : 0\n\nFailed PIDs : []'.format(time.time(), start, stop, self.t()))
                file.close()
        else :
            try :

                with open(fileName, 'r') as file :
                    data = file.readlines()
                    data[4+2] = '{}\n'.format(self.getTimeElapsed(fileName))
                    data[6+2] = 'Total number of checks : {}\n'.format(checks)
                    data[8+2] = 'Last check time {}\n'.format(checkTime)
                    data[10+2] = 'Failed gets : {}\n'.format(fails)
                    data[12+2] = 'Failed PIDs : {}\n'.format(failList)
                    file.close()

                with open(fileName, 'w') as file :
                    file.writelines(data)
                    file.close()

            except Exception as e :
                recurRate += 1
                if recurRate == 5:
                    print (e)
                    print ('[{}] : Failed to write {}, checks - {}, check time {}, fails - {}'.format(self.t(), fileName, checks, checkTime, fails))
                else :
                    print ('[{}] : Error writing {}, retring, try number {}'.format(self.t(), fileName, recurRate))
                    self.scrapeImageWrite(fileName, recurRate, start, stop, checks, checkTime, fails, failList)

    def scrapeRestockWrite(self, fileName, recurRate, checks, checkTime, fails, sizes ):

        try :
            with open(fileName, 'r') as file :
                data = file.readlines()
                data[4+2] = '{}\n'.format(self.getTimeElapsed(fileName))
                data[6+2] = 'Checks : {}\n'.format(checks)
                data[8+2] = 'Fails : {}\n'.format(fails)
                data[10+2] = 'Last check time {}\n'.format(round(checkTime, 2))
                file.close()

            with open(fileName, 'w') as file :
                file.writelines(data)
                file.close()

            if len(sizes) > 0:
                with open(fileName, 'a') as file :
                    file.writelines('\n\n[{}] : {} restocked'.format(self.t(), ', '.join(sizes)))
                    file.close()

        except Exception as e :
            recurRate += 1
            if recurRate == 5:
                print (e)
                print ('[{}] : Failed to write {}, checks - {}, check time {}, fails - {}, sizes restocked - {}'.format(self.t(), fileName, checks, checkTime, fails, sizes))
            else :
                print ('[{}] : Error writing {}, retring, atmept number {}'.format(self.t(), fileName, recurRate))
                self.scrapeRestockWrite( fileName, recurRate, checks, checkTime, fails, sizes )

    def scrapeUpdateWrite(self, fileName, recurRate, pid, checks, checkTime, fails):

        if checks == 0:
            with open(fileName, 'w+') as file :
                file.writelines('{}\n\nUpdate : {}\n\nStart time : [{}]\n\nTime elapsed : [0]\n\nTotal number of checks : 0\n\nLast check time : 0\n\nFailed gets : 0\n'.format(time.time(), pid, self.t()))
                file.close()
        else :
            try :
                with open(fileName, 'r') as file :
                    data = file.readlines()
                    data[4+2] = '{}\n'.format(self.getTimeElapsed(fileName))
                    data[6+2] = 'Total number of checks : {}\n'.format(checks)
                    data[8+2] = 'Last check time {}\n'.format(checkTime)
                    data[10+2] = 'Failed gets : {}\n'.format(fails)
                    file.close()

                with open(fileName, 'w') as file :
                    file.writelines(data)
                    file.close()
            except Exception as e :
                recurRate += 1

                if recurRate == 5:
                    print (e)
                    print ('[{}] : Failed to write {}, checks - {}, check time {}, fails - {}'.format(self.t(), fileName, checks, checkTime, fails))
                else :
                    print ('[{}] : Error writing {}, retring, atempt number {}'.format(self.t(), fileName, recurRate))
                    self.scrapeUpdateWrite(fileName, recurRate, pid, checks, checkTime, fails)

class MisilaniousFunctions:

    def t(self):
        try :
            now = datetime.datetime.now(timezone('US/Eastern'))
        except :
            now = datetime.datetime.now()

        return '{}/{}/{}-{}:{}:{}'.format(now.month, now.day, now.year, now.hour, now.minute, now.second)

    def clearImages(self):
        while True:
            time.sleep(60 * 60 * 4)
            for file in list(f for f in os.listdir('.') if os.path.isfile(f)):
                if '.jpg' in file:
                    os.remove(file)

    def clearFiles(self, argList, notList):
        for file in list(f for f in os.listdir('.') if os.path.isfile(f)):
            if any(kw in file for kw in argList) and file not in notList:
                os.remove()

    def makeHaste(self, text):
        r = requests.post('https://hastebin.com/documents', data = text)
        key = json.loads(r.text)['key']
        return 'https://hastebin.com/{}.txt'.format(key)

    def filter(self, text):
        passed = False

        kwList = [
            ['yeezy'],
            ['yzy'],
            ['kanye'],
            ['boost'],
            ['consitorium'],
            ['triple', 's', 'balenciaga'],
            ['adidas', 'nmd'],
            ['adidas', 'prime', 'knit'],
            ['nmd', 'boost'],
            ['nike', 'flyknit'],
            ['nike', 'racer'],
            ['nike', 'basketball'],
            ['nike', 'lab'],
            ['nike', 'retro'],
            ['nike', 'original'],
            ['nike', 'jordan'],
            ['nike', 'air', 'max'],
            ['jordan', 'retro'],
            ['jordan', 'all', 'star'],
            ['jordan', '1'],
            ['jordan', '2'],
            ['jordan', '3'],
            ['jordan', '4'],
            ['jordan', '5'],
            ['jordan', '6'],
            ['jordan', '7'],
            ['jordan', '8'],
            ['jordan', '9'],
            ['jordan', '10'],
            ['jordan', '11'],
            ['jordan', '12'],
            ['jordan', '13'],
            ['jordan', '14'],
            ['jordan', '15'],
            ['jordan', '20'],
            ['jordan', '23'],
            ['350', 'boost'],
            ['350', 'yeezy'],
            ['350', 'yzy'],
            ['350', 'v2'],
            ['750', 'boost'],
            ['750', 'yeezy'],
            ['750', 'yzy'],
            ['750', 'v2'],
            ['adidas', '4d']
            ]


        for k in kwList:
            if all(kw in text.lower() for kw in k):
                passed = True
                break

        return passed

    def normalizeText(self, txt):


        try :
            txt = str(txt)
        except :
            txt = unicodedata.normalize('NFKD', ''.join(txt.strip())).encode('ascii','ignore')


        indexs = []
        sr = ''

        strList = list(txt)

        for i in range(1, len(txt)-1):
            if strList[i] == ' ':
                if strList[i-1] == ' ' or strList[i+1] == ' ':
                    indexs.append(i)

            if strList[i] in ['\n', '\t', '\r'] :
                indexs.append(i)

        for i in range(0, len(strList)):
            if i not in indexs:
                sr += strList[i]

        if sr[0] == ' ':
            sr = sr[1:len(sr)-1]
        if sr[len(sr)-1] == ' ':
            sr = sr[0:len(sr) - 2]

        return sr

    def parseName(self, productURL):
        i = len(productURL) - 1

        if i > 0:
            i = ( i - 1 if productURL[i] == '/' else i)

            while i >= 0:
                char = productURL[i]
                if char == '/':
                    index = i
                    break
                else:
                    pass

                pass

                i -= 1

            productURL = (productURL[0:len(productURL) - 1] if productURL[len(productURL) - 1] == '/' else productURL)
            productURL = productURL.replace((productURL[0:index + 1]), '')
            productURL = productURL.replace('-', ' ').replace('.html', '')
        else :
            productURL = 'Null Product Title'

        return productURL

    def getRandString(self):
        aList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't','u', 'v', 'w', 'x', 'y', 'z']
        string = ''

        for i in range(0, 30):
            string += aList[random.randint(0, 23)]

        return string + '.jpg'

    def meshCommerceIsLoaded(self, site, pid):

        apiKey, userAgent, abrev = self.getMeshHeaders(site)
        scrapeUrl = 'https://commerce.mesh.mx/stores/{}/products/{}'.format(site, pid)

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

        r = requests.get(scrapeUrl, headers = headers)

        if r.status_code == 200:
            url = json.loads(r.text)['URL']
            name = json.loads(r.text)['name']
        else :
            url = False
            name = False

        return url, name

    def bnyIsLoaded(self, pid):

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

        r = requests.get('https://www.barneys.com/rest/model/barneys/commerce/catalog/BNYProductDetailDisplayActor/getProductDetailsPageInfo?productId={}'.format(pid) , headers = headers)

        if r.text == 'No records fetched for the product 503172407':
            data = json.loads(r.text)
            prodData = json.loads(json.dumps(data['productDetails']))
            prodData2 = json.loads(json.dumps(prodData[0]))
            atrData = json.loads(json.dumps(prodData2['attributes']))
            name = self.normalizeText(atrData['product.displayName'][0])
            url = 'http://www.barneys.com/' + str(atrData['product.productDetailPageUrl'][0])
        else :
            name = False
            url = False


        return url, name

    def isMesh(self, url):
        url = url.lower()
        if 'www.footpatrol.co.uk' in url:
            mesh = True
        elif 'www.size.co.uk' in url:
            mesh = True
        elif 'www.jdsports.co.uk' in url:
            mesh = True
        elif 'www.tessuti.co.uk' in url:
            mesh = True
        else :
            mesh = False

        return mesh

    def quote(self, text):
        return '"{}"'.format(text)

    def getMeshHeaders(self, site):

        if site == "footpatrol":
            apiKey = '5F9D749B65CD44479C1BA2AA21991925'
            userAgent = 'FootPatrol/2.0 CFNetwork/808.1.4 Darwin/16.1.0'
            abrev = 'fp'

        elif site == "size":
            apiKey = 'EA0E72B099914EB3BA6BE90A21EA43A9'
            userAgent = 'Size-APPLEPAY/4.0 CFNetwork/808.1.4 Darwin/16.1.0'
            abrev = 'sz'

        elif site == "jdsports":
            apiKey = '1A17CC86AC974C8D9047262E77A825A4'
            userAgent = 'JDSports/5.3.1.207 CFNetwork/808.1.4 Darwin/16.1.0'
            abrev = 'jd'

        elif site == "tessuti":
            apiKey = '8A744E893B794A3EA3C0497352FD8309'
            userAgent = 'Tessuti-APPLEPAY/2.0.0.1 CFNetwork/808.1.4 Darwin/16.1.0'
            abrev = 'te'

        return apiKey, userAgent, abrev

    def isShop(self, url):
        r = requests.get(url+'.json')
        return (True if r.status_code == 200 else False )

    def isUrl(self, url):
        try :
            requests.get(url)
            url = True
        except:
            url = False

        return url

    def isShopStock(self, url):

        jLink = url + '.json'
        sess = requests.Session()

        req = self.getRequ(sess, jLink, {}, "Shop Test {}".format(url))
        Jdata = json.loads(req.text)

        productJson = json.loads(json.dumps(Jdata['product']))
        variantJson = json.loads(json.dumps(productJson['variants']))
        vJson = json.loads(json.dumps(variantJson[0]))

        try :
            vJson['inventory_quantity']
            selector = True
        except :
            selector = False

        return selector

    def runFunctions(self, fileName):

        while True :

            for i in self.socketRecive() :

                functTitle = i[0]

                if functTitle == 'textRestock':
                    Process(target = self.textRestock, args = (i[1], i[2], i[3], i[4], i[5], i[6], i[7], )).start()
                    callString = 'Process(target = self.textRestock, args = ({}, {}, {}, {}, {}, {}, {})).start()'.format(i[1], i[2], i[3], i[4], i[5], i[6], i[7])
                    self.writePythonFile(fileName, callString)

                elif functTitle == 'pageRestock':
                    Process(target = self.pageContentChange, args = (i[1], i[2], i[3], i[4], )).start()
                    callString = 'Process(target = self.pageContentChange, args = ({}, {}, {}, {})).start()'.format(i[1], i[2], i[3], i[4])
                    self.writePythonFile(fileName, callString)

                elif functTitle == 'codeChange':
                    Process(target = self.codeChange, args = (i[1], i[2], i[3], i[4], )).start()
                    callString = 'Process(target = self.codeChange, args = ({}, {}, {}, {})).start()'.format(i[1], i[2], i[3], i[4])
                    self.writePythonFile(fileName, callString)

                elif functTitle == 'shopRestock':
                    Process(target = self.shopRestock, args = (i[1], i[2], )).start()
                    callString = 'Process(target = self.shopRestock, args = ({}, {})).start()'.format(i[1], i[2])
                    self.writePythonFile(fileName, callString)

                elif functTitle == 'meshCommerceRestock':
                    Process(target = self.meshCommerceRestock, args = (i[1], i[2], )).start()
                    callString = 'Process(target = self.meshCommerceRestock, args = ({}, {})).start()'.format(i[1], i[2])
                    self.writePythonFile(fileName, callString)

                elif functTitle == 'barneyPIDrestock':
                    Process(target = self.barneyPIDrestock, args = (i[1], i[2], )).start()
                    callString = 'Process(target = self.barneyPIDrestock, args = ({}, {})).start()'.format(i[1], i[2])
                    self.writePythonFile(fileName, callString)

                elif functTitle == 'meshCommerceCheckPID':
                    Process(target = self.meshCommerceCheckPID, args = (i[1], i[2], )).start()
                    callString = 'Process(target = self.meshCommerceCheckPID, args = ({}, {})).start()'.format(i[1], i[2])
                    self.writePythonFile(fileName, callString)

                elif functTitle == 'barneyPIDscrape':
                    Process(target = self.barneyPIDscrape, args = (i[1], )).start()
                    callString = 'Process(target = self.barneyPIDscrape, args = ({},)).start()'.format(i[1])
                    self.writePythonFile(fileName, callString)

                elif functTitle == 'sneakerStock':
                    Process(target = self.stockX, args = (i[1], i[2], )).start()
                    callString = 'Process(target = self.stockX, args = ({}, {})).start()'.format(i[1], i[2])
                    self.writePythonFile(fileName, callString)

                elif functTitle == 'getSneakerStock':
                    Process(target = self.returnStockHaste, args = (i[0], )).start()

    def stripFunction(self, string):
        return string.replace('Process', '').replace('Thread', '').replace('#', '').replace('"', '').replace("'", '').replace('(', '').replace(')', '').replace('.start', '').replace(' ', '').strip()

    def returnDataString(self, text):
        return ''.join(text).replace(' ', '')

    def getFunctionsInFile(self, file):

        functionData = []

        with open(file, 'r') as file :
            data = file.readlines()

        for i in data :

            if (('Process(' in i) or ('Thread(' in i)) and ('#' not in i ):
                string = self.stripFunction(i)
                functionData.append(string)

        return ''.join(functionData)

class SocketsMessage:

    def getSendy(self, connection, data):

        data = data if type(data) == list else [data]

        jData = json.dumps(data)
        send =  '{}{}'.format(len(jData), jData).encode()
        connection.sendall(send)

    def getRecvy(self, connection):
        ln = connection.recv(30).decode()
        string = ''
        data = []
        for i in range(0, 30):
            try :
                int(ln[i])
                string += ln[i]
            except :
                break

        msgLn = int(string)
        msgLn = msgLn - (len(ln) - len(string))
        data.append(ln[len(string):])

        while msgLn != 0 :
            tempdata = connection.recv(msgLn).decode()
            data.append(tempdata)
            msgLn -= len(tempdata)

        return json.loads(''.join(data))

    def socketRecive(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try :
            s.bind(('', 3434))
        except :
            s.close()
            print ("{} Failed to accept new connections, retrying in 30 sec", self.t())
            time.sleep(30)
            self.socketRecive()

        s.listen(1)
        c, a = s.accept()

        data = self.getRecvy(c)

        '''
        if (data)[0] == 'currentProcesses':
            self.getSendy(c, self.getFunctionsInFile(file))
        else :
            self.getSendy(c, 'Data Recived')
        '''
        self.getSendy(c, 'Data Recived')

        c.close()

        return data

    def socketSend(self, ip, functData):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try :
            s.connect((ip, 3434))
        except Exception as e :
            print (e)
            print ('{} Failed to establish connection to {}, retrying in 30 sec'.format(self.t(), ip))
            s.close()
            time.sleep(30)
            self.socketSend( ip, functData)

        self.getSendy(s, functData)
        data = self.getRecvy(s)
        s.close()

        return data







