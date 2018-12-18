
## Multi threaded advanced page monitor developed and designed by Lyle Londraville / @SoleWingSneaks

import tkMessageBox , smtplib, Tkinter, requests, datetime, threading, time, csv, tweepy 
from Tkinter import *
import Tkinter as tk 
from ScrolledText import *
from bs4 import BeautifulSoup
from threading import Thread
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone

####################################################################################################################################################################################################################



global app 
global mb
global link
global baseLink
global Gspan
global Gclass
global Gname
global threadName
global proxy
global consoleLog
global threadLog
global keyword
global cancleKey
global server
global proxyCheckVar
global keywordCheckVar
global redirectVar
global Tvar 
global stopThreadList
global stopENTRYstr
global Tlist 
global saveIndexList
global tweeList

tweeList = []
saveIndexList = []
Tlist = []
stopThreadList = []




####################################################################################################################################################################################################################

def logWrite(box, name, text):
        cur_time = datetime.now()
        print_time = cur_time.strftime('%H-%M-%S')
        box.configure(state = 'normal')
        box.insert(END, (print_time + ' : '+ name + ' > '+text))
        box.configure(state = 'disabled')

def TlogWrite(box, text):

        cur_time = datetime.now()
        print_time = cur_time.strftime('%H-%M-%S')
        box.configure(state = 'normal')
        box.insert(END, (print_time + ' : ' + text + '\n'))
        box.configure(state = 'disabled')


def addTweeAuth():
    
    global ConsumerKey
    global ConsumerSecret
    global AccessToken
    global AccessTokenSecret

    def csvWriteTwee():

        tweeList.append(ConsumerKey.get())
        tweeList.append(ConsumerSecret.get())
        tweeList.append(AccessToken.get()) 
        tweeList.append(AccessTokenSecret.get())


        c = open('TweeAuth.csv', 'w')

        wtr = csv.writer(c)
        wtr.writerow(tweeList)

        c.close()

        tweeList[:] = []

        tkMessageBox.showinfo( "", 'Twitter auth info saved!')
    

    tweeWin = Toplevel(app)

    sws = app.winfo_screenwidth() 
    shs = app.winfo_screenheight() 

    sx = ((sws/2)) - 150
    sy = ((shs/2)) -400
    tweeWin.geometry('%dx%d+%d+%d' % (410, 210, sx, sy))
    tweeWin.title('')
    tweeWin.configure(bg = 'gray23')  
    

    ConsumerKeyl = Label(tweeWin, text = 'Consumer Key', background = 'gray23', fg = 'white')
    ConsumerKeyl.place(x = 15, y = 25)
    ConsumerKey = Entry(tweeWin, bd = 0, width = 25, background = 'white')
    ConsumerKey.place(x = 150, y = 25)

    ConsumerSecretl = Label(tweeWin, text = 'Consumer Secret', background = 'gray23', fg = 'white')
    ConsumerSecretl.place(x = 5, y = 60)
    ConsumerSecret = Entry(tweeWin, bd = 0, width = 25, background = 'white')
    ConsumerSecret.place(x = 150, y = 60)

    AccessTokenl = Label(tweeWin, text = 'Access Token', background = 'gray23', fg = 'white')
    AccessTokenl.place(x = 15, y = 95)
    AccessToken = Entry(tweeWin, bd = 0, width = 25, background = 'white')
    AccessToken.place(x = 150, y = 95)

    AccessTokenSecretl = Label(tweeWin, text = 'Access Token Secret', background = 'gray23', fg = 'white')
    AccessTokenSecretl.place(x = 5, y = 130)
    AccessTokenSecret = Entry(tweeWin, bd = 0, width = 25, background = 'white')
    AccessTokenSecret.place(x = 150, y = 130)

    text = open('TweeAuth.csv')
    data = csv.reader(text)

    for i in data :
        ConsumerKey.insert(0, str(i[0]) )
        ConsumerSecret.insert(0, str(i[1]) )
        AccessToken.insert(0, str(i[2]) )
        AccessTokenSecret.insert(0, str(i[3]) )


    saveBtn = Button(tweeWin, text = 'Save', bd = 0, highlightbackground = 'gray23', fg = 'white', height = 1, width = 11, command = csvWriteTwee)
    saveBtn.pack(fill = Y, side = BOTTOM, pady = 14)




def tweeAuth():
    
    global twee

    try :
        text = open('TweeAuth.csv')
        lis = csv.reader(text)

        for i in lis :
            CONSUMER_KEY = str(i[0])
            CONSUMER_SECRET = str(i[1])   
            ACCESS_KEY = str(i[2])   
            ACCESS_SECRET = str(i[3])

        if (CONSUMER_KEY or CONSUMER_SECRET or ACCESS_KEY or ACCESS_SECRET) == '':
            tkMessageBox.showinfo( "Error!", 'Not all Twitter auth keys were filled out successfully!')
        
        else :

            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

            twee = tweepy.API(auth)

            return twee 

        #tkMessageBox.showinfo('', 'Successfully authenticated Twitter!')

    except :
        tkMessageBox.showinfo('Error!', 'Could not authenticate Twitter!')

def tweeLogin():
    global twee
    twee = tweeAuth()
    return twee 

def message(text): 
    twee.update_status(text)


def getReq(url, prxy, alwReD, errorMSG) :

        proxies = {
                'https': ('https://%s' % prxy)
                }

        if prxy == '':
                try :
                        page = requests.get(url, allow_redirects = alwReD)
                except :
                        logWrite(consoleLog, Tname, (errorMSG + '\n'))

        else :
                try :
                        page = requests.get(url, proxies = proxies, allow_redirects = alwReD)
                except :
                        logWrite(consoleLog, Tname, 'Failed to establish connection with proxy! Using regular connection.\n')
                        try :
                                page = requests.get(url, allow_redirects = alwReD)
                        except :
                                logWrite(consoleLog, Tname, (errorMSG + '\n'))
        return page

def compareLinks(old, new, t1, t2, baseurl, item, kw, Tname):

        cont = 0

        for link in new :
                if (link not in old) :
                        if (kw in link):
                                message((baseurl+link))
                                old.append(link)
                                cont += 1

        new[:] = []

        consoleMessage =  'Looptime - ' + (str(round((t2-t1), 2))) + ', found ' + str(cont) + ' ' + item + '\n'
        logWrite(consoleLog, Tname, consoleMessage)



def stopNameWin():
    
    def parseStopString():
        stopThreadList[:] = []

        string = stopENTRYstr.get()
        strlen = len(string)-1
        startlen = 0
        tempstr = ''

        while startlen <= (len(string)-1) :
            char = string[startlen]
            
            if startlen == (len(string)-1) :
                tempstr += char
                stopThreadList.append(tempstr)
            
            else :
                if char != ',':
                    tempstr += char
                else :
                    stopThreadList.append(tempstr)
                    tempstr = '' 
            startlen += 1 
        tkMessageBox.showinfo( "", 'Threads killed!')


    
    stopWin = tk.Toplevel(app)

    sws = app.winfo_screenwidth() 
    shs = app.winfo_screenheight() 

    sx = ((sws/2)) - 150
    sy = ((shs/2)) -400
    stopWin.geometry('+%d+%d' % (sx, sy))
    stopWin.title('')
    stopWin.configure(bg = 'gray23')  
    

    stopThreadStringl = Label(stopWin, text = 'Enter threads separated by a comma and no spaces', background = 'gray23', fg = 'white')
    stopThreadStringl.pack()
    stopENTRYstr = Entry(stopWin, bd = 0, width = 23, background = 'white')
    stopENTRYstr.pack()

    stopStrBtn = Tkinter.Button(stopWin, text = 'STOP', bd = 0, highlightbackground = 'gray23', fg = 'white', height = 1, width = 11, command = parseStopString)
    stopStrBtn.pack()

    
    lb = Label(stopWin, text = "Currently running threads", background = 'gray23', fg = 'white')
    lb.pack()

    lb2 = Label(stopWin, text = "", background = 'gray23', fg = 'white')
    lb2.pack()

    if len(Tlist) > 0 :

        for i in Tlist:

            L = Label(stopWin, text = i, background = 'gray23', fg = 'white')
            L.pack()
    else :

            L = Label(stopWin, text = 'You currently have no threads running', background = 'gray23', fg = 'white')
            L.pack()



def csvWrite():

    c = open('Sites.csv', 'w')

    wtr = csv.writer(c)
    for i in saveIndexList :
        wtr.writerow(i)

    c.close()


def importThreads() :
    
    text = open('Sites.csv')
    lis = csv.reader(text)

    for i in lis :
        typeFunct = i[0]

        if typeFunct == 'Link':
            T = Thread(target = LinkFunct, args = (str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6]), str(i[7]), str(i[8]), i[9], str(i[10]),))
            T.start()
            Tlist.append(str(i[10]))
        elif typeFunct == 'A-link':
            T = Thread(target = AlinkFunct, args = (str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), i[6], str(i[7]),))
            T.start()
            Tlist.append(str(i[7]))
        elif typeFunct == 'H-link' :
            T = Thread(target = HlinkFunct, args = (str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6]), str(i[7]), str(i[8]), i[9], str(i[10]),))
            T.start()
            Tlist.append(str(i[10]))
        elif typeFunct == 'Monitor HTML' :
            T = Thread(target = itemFunct, args = (str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6]), i[7], str(i[8]),))
            T.start()   
            Tlist.append(str(i[8]))
        elif typeFunct == 'Status Code' :
            T = Thread(target = codeFunct, args = (str(i[1]), str(i[2]), str(i[3]), i[4], str(i[5]),))
            T.start()
            Tlist.append(str(i[5]))
        elif typeFunct == 'Shopify sitemap' :
            T = Thread(target = ShofSitemapFunct, args = (str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]),))
            T.start()
            Tlist.append(str(i[5]))
        elif typeFunct == 'Shopify restock' :
            T = Thread(target = ShofRestockFunct, args = (str(i[1]), str(i[2]), str(i[3]), str(i[4]),))
            T.start()
            Tlist.append(str(i[4]))
        elif typeFunct == 'Supreme restock' :
            T = Thread(target = supRestockFunct, args = (str(i[1]), str(i[2]), str(i[3]), str(i[4]),))
            T.start()
            Tlist.append(str(i[4]))
        else :
            tkMessageBox.showinfo( "Error!", 'Something went wrong, try again.')


####################################################################################################################################################################################################################

def itemFunct(url, span, clas, name, prxy, tm, alwReD, Tname):

    old = []
    new = []
    onVar = True

    logWrite(consoleLog, Tname, 'Started task!\n')
    threadLog.insert(END, (Tname+'\n'))

    oldSoup = BeautifulSoup((getReq(url, prxy, alwReD, 'Failed to create initial index')).content, 'html.parser')
    oldItem = oldSoup.find(span, {clas : name})
    old.append(oldItem)

    if tm == '':
        tm = 0
    else :
        pass 

    while onVar == True :
             

            time.sleep(int(tm))

            t1 = time.time()

            newSoup = BeautifulSoup((getReq(url, prxy, alwReD, 'Failed to refresh item')).content, 'html.parser')
            newItem = newSoup.find(span, {clas : name})
            new.append(newItem)

            t2 = time.time()

            if new != old :
                    message('leelthefantabulous@gmail.com', 'Leelis40', '3306031362@vtext.com', ('Page update!\n'+url))
                    old[:] = []

                    repSoup = BeautifulSoup((getReq(url, prxy, alwReD, 'links')).content, 'html.parser')
                    repItem = repSoup.find(span, {clas : name})
                    old.append(repItem)

                    new[:] = []

                    consoleMessage =  'Looptime : ' + (str(round((t2-t1), 2))) + ', page change!\n '

            else :
                    new[:] = []
                    consoleMessage =  'Looptime : ' + (str(round((t2-t1), 2))) + ', zero page changes\n '

            logWrite(consoleLog, Tname, consoleMessage)

            if Tname in stopThreadList :
                onVar += 1
                logWrite(consoleLog, Tname, 'Thread killed!\n')
                stopThreadList.remove(Tname)
                Tlist.remove(Tname)
            else :
                pass

def codeFunct(url, prxy, tm, alwReD, Tname):

    new = []
    old = []
    onVar = 1

    logWrite(consoleLog, Tname, 'Started task!\n')
    

    old.append((getReq(url, prxy, alwReD, 'Failed to check for initial code')).status_code)

    if tm == '':
        tm = 0
    else :
        pass 
    
    while onVar == 1 :


            time.sleep(int(tm))

            t1 = time.time()

            new.append((getReq(url, prxy, alwReD, 'Failed to check status code')).status_code)

            t2 = time.time()

            if new != old :
                message('leelthefantabulous@gmail.com', 'Leelis40', '3306031362@vtext.com', ('Status code change!\n'+url))
                old[:] = []
                old.append((getReq(url, prxy, alwReD, 'Could not check for new status code')).status_code)
                new[:] = []

                consoleMessage =  'Looptime : ' + (str(round((t2-t1), 2))) + ', status code change!\n '

            else :
                new[:] = []
                consoleMessage =  'Looptime : ' + (str(round((t2-t1), 2))) + ', zero code changes\n '

            logWrite(consoleLog, Tname, consoleMessage)
            
            if Tname in stopThreadList :
                onVar += 1
                logWrite(consoleLog, Tname, 'Thread killed!\n')
                stopThreadList.remove(Tname)
                Tlist.remove(Tname)
            else :
                pass 


def supRestockFunct(url, prxy, tm, Tname):

        old = []
        new = []
        onVar = True

        logWrite(consoleLog, Tname, 'Started task!\n')
        

        headers = {
            'Host': 'www.supremenewyork.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8'
        }


        oldSoup = BeautifulSoup((getReq(url, prxy, False, 'Failed to gather initial links')).content, 'html.parser')
        title = oldSoup.find('h1',{'itemprop':'name'}).text
        color = oldSoup.find('p',{'class':'style'}).text
        msgSTR =  title + ' ' + color + '\n' + 'Sizes : '

        for item in oldSoup(id = 'size'):
            old.append(item.text)

        if tm == '':
            tm = 0
        else :
            pass 

        while onVar == True :

                 

                cont = 0

                time.sleep(int(tm))

                t1 = time.time()

                newSoup = BeautifulSoup((getReq(url, prxy, False, 'Failed to check for new sizes')).content, 'html.parser')
                for item in newSoup(id = 'size'):
                    new.append(item.text)

                t2 = time.time()

                for size in new :
                    if size not in old :
                        msgSTR += (size + '\n')
                        cont += 1

                if cont > 0 :
                    msgSTR += url
                    message('leelthefantabulous@gmail.com', 'Leelis40', '3306031362@vtext.com',(msgSTR))
                    old[:] = []
                    old = new

                else :
                    pass

                new[:] = []

                logWrite(consoleLog, Tname, ('Loop time : %s, %s sizes restocked' % ((str(round((t2-t1), 2))), cont)))

                if Tname in stopThreadList :
                    onVar += 1
                    logWrite(consoleLog, Tname, 'Thread killed!\n')
                    stopThreadList.remove(Tname)
                    Tlist.remove(Tname)
                else :
                    pass
## Needs testing
def ShofSitemapFunct(sitemap, prxy, tm, kw, Tname):

    old = []
    new = []
    onVar = True

    logWrite(consoleLog, Tname, 'Started task!\n')
    

    soup = BeautifulSoup((getReq(url, prxy, False, 'Failed to gather initial links')).content, 'html.parser')
    for item in soup.find_all('url'):
        old.append(item.loc.text)

    if tm == '':
        tm = 0
    else :
        pass 

    while onVar == True :

             

            time.sleep(int(tm))

            t1 = time.time()

            newSoup = BeautifulSoup((getReq(url, prxy, False, 'Failed to check for new links')).content, 'html.parser')
            for item in newSoup.find_all('url'):
                new.append(item.loc.text)

            t2 = time.time()

            compareLinks(old, new, t1, t2, '', 'links', kw, Tname)

            if Tname in stopThreadList :
                onVar += 1
                logWrite(consoleLog, Tname, 'Thread killed!\n')
                stopThreadList.remove(Tname)
                Tlist.remove(Tname)
            else :
                pass
## Needs testing
def ShofRestockFunct(url, prxy, tm, Tname):

        old = []
        new = []
        onVar = True

        logWrite(consoleLog, Tname, 'Started task!\n')
        

        oldDict1 = json.loads(((getReq((url + '.json'), prxy, False, 'Failed to get initial sizes'))).text)
        oldDict2 = json.loads(json.dumps(oldDict1['product']))
        msgSTR += (json.dumps(oldDict2['title']) + '\n' + 'Sizes ')
        oldDict3 = json.loads(json.dumps(oldDict2['variants']))

        for i in oldDict3:
            if json.dumps(i['inventory_quantity']) == '0' :
                old.append(json.dumps(i['title']))

        if tm == '':
            tm = 0
        else :
            pass 

        while onVar == True :

                 

                time.sleep(int(tm))

                t1 = time.time()

                newDict1 = json.loads(((getReq((url + '.json'), prxy, False, 'Failed to check for new sizes'))).text)
                newDict2 = json.loads(json.dumps(newDict1['product']))
                newDict3 = json.loads(json.dumps(newDict2['variants']))

                for i in newDict3:
                    if json.dumps(i['inventory_quantity']) == '0' :
                        new.append(json.dumps(i['title']))

                t2 = time.time()

                compareLinks(old, new, t1, t2, '', 'new sizes', '', Tname)

                if Tname in stopThreadList :
                    onVar += 1
                    logWrite(consoleLog, Tname, 'Thread killed!\n')
                    stopThreadList.remove(Tname)
                    Tlist.remove(Tname)
                else :
                    pass
## Needs testing

def HlinkFunct(url, baseurl, span, clas, name, prxy, tm, kw, alwReD, Tname):

        old = []
        new = []
        onVar = True

        logWrite(consoleLog, Tname, 'Started task!\n')
        

        oldSoup = BeautifulSoup(((getReq(url, prxy, alwReD, 'Failed to gather initial links'))).content,'html.parser')
        oldLinks = oldSoup.find_all(span ,{clas : name})

        for link in oldLinks :
                old.append(str(link['href']))

        if tm == '':
            tm = 0
        else :
            pass 

        while onVar == True :

                 

                time.sleep(int(tm))

                t1 = time.time()

                newSoup = BeautifulSoup(((getReq(url, prxy, alwReD, 'Failed to check for new links'))).content,'html.parser')
                newLinks = newSoup.find_all(span ,{clas : name})

                for link in newLinks:
                        new.append(str(link['href']))
                t2 = time.time()

                compareLinks(old, new, t1, t2, baseurl, 'links', kw, Tname)

                if Tname in stopThreadList :
                    onVar += 1
                    logWrite(consoleLog, Tname, 'Thread killed!\n')
                    stopThreadList.remove(Tname)
                    Tlist.remove(Tname)
                else :
                    pass
## Needs testing

def LinkFunct(url, baseurl, span, clas, name, prxy, tm, kw, alwReD, Tname):

        old = []
        new = []
        onVar = True

        logWrite(consoleLog, Tname, 'Started task!\n')
        

        oldSoup = BeautifulSoup((getReq(url, prxy, alwReD, 'Failed to gather initial links')).content, 'html.parser')
        oldLinks = oldSoup.find_all(span ,{clas : name})
        for link in oldLinks:
                old.append(str(link.a['href']))


        if tm == '':
            tm = 0
        else :
            pass 

        while onVar == True :

                 

                time.sleep(int(tm))

                t1 = time.time()

                newSoup = BeautifulSoup((getReq(url, prxy, alwReD, 'Failed to check for new links')).content,'html.parser')
                newLinks = newSoup.find_all(span ,{clas : name})
                for link in newLinks:
                        new.append(str(link.a['href']))

                t2 = time.time()

                compareLinks(old, new, t1, t2, baseurl, 'links', kw, Tname)

                if Tname in stopThreadList :
                    onVar += 1
                    logWrite(consoleLog, Tname, 'Thread killed!\n')
                    stopThreadList.remove(Tname)
                    Tlist.remove(Tname)
                else :
                    pass

def AlinkFunct(url, baseurl, prxy, tm, kw, alwReD, Tname):

        old = []
        new = []
        onVar = True

        logWrite(consoleLog, Tname, 'Started task!\n')
        

        req = (getReq(url, prxy, alwReD, 'Failed to gather initial links'))

        oldSoup = BeautifulSoup(req.content, 'html.parser')
        oldLinks = oldSoup.find_all('a')

        for link in oldLinks:
                old.append(str(link.get('href')))

        if tm == '':
            tm = 0
        else :
            pass 

        while onVar == True :

                 

                time.sleep(int(tm))

                t1 = time.time()

                newSoup = BeautifulSoup((getReq(url, prxy, alwReD, 'Failed to check for new links')).content, 'html.parser')
                newLinks = newSoup.find_all('a')

                for link in newLinks:
                        new.append(str(link.get('href')))

                t2 = time.time()

                compareLinks(old, new, t1, t2, baseurl, 'links', kw, Tname)

                if Tname in stopThreadList :
                    onVar += 1
                    logWrite(consoleLog, Tname, 'Thread killed!\n')
                    stopThreadList.remove(Tname)
                    Tlist.remove(Tname)
                else :
                    pass


####################################################################################################################################################################################################################

def pickFunct():

        option = mb.get()
        miniSaveList = []

        if (threadName.get()) not in Tlist:
            if option == 'Link':

                    if ((link.get() and Gspan.get() and Gclass.get() and Gname.get() and threadName.get()) != '') == True :
                            T = Thread(target = LinkFunct, args = (link.get(), baseLink.get(), Gspan.get(), Gclass.get(), Gname.get(), proxy.get(), timeout.get(), keyword.get(), checkRedirect(), threadName.get() ))
                            T.start()
                            Tlist.append(threadName.get())
                            miniSaveList[:] = []
                            miniSaveList.append('link')
                            miniSaveList.append(link.get())
                            miniSaveList.append(baseLink.get())
                            miniSaveList.append(Gspan.get())
                            miniSaveList.append(Gclass.get())
                            miniSaveList.append(Gname.get())
                            miniSaveList.append(proxy.get())
                            miniSaveList.append(timeout.get())
                            miniSaveList.append(keyword.get())
                            miniSaveList.append(checkRedirect())
                            miniSaveList.append(threadName.get())
                            saveIndexList.append(miniSaveList)

                    else :
                            tkMessageBox.showinfo( "Error!", 'Not all values were filled out correctly!')

            elif option == 'A-link':

                    if ((link.get() and threadName.get()) != '') == True :
                            T = Thread(target = AlinkFunct, args = (link.get(), baseLink.get(), proxy.get(), timeout.get(), keyword.get(), checkRedirect(), threadName.get() ))
                            T.start()
                            Tlist.append(threadName.get())
                            miniSaveList[:] = []
                            miniSaveList.append('A-link')
                            miniSaveList.append(link.get())
                            miniSaveList.append(baseLink.get())
                            miniSaveList.append(proxy.get())
                            miniSaveList.append(timeout.get())
                            miniSaveList.append(keyword.get())
                            miniSaveList.append(checkRedirect())
                            miniSaveList.append(threadName.get())
                            saveIndexList.append(miniSaveList)

                    else :
                            tkMessageBox.showinfo( "Error!", 'Not all values were filled out correctly!')

            elif option == 'H-link':

                    if ((link.get() and Gspan.get() and Gclass.get() and Gname.get() and threadName.get()) != '') == True  :
                            T = Thread(target = HlinkFunct, args = (link.get(), baseLink.get(), Gspan.get(), Gclass.get(), Gname.get(), proxy.get(), timeout.get(), keyword.get(), checkRedirect(), threadName.get()))
                            T.start()
                            Tlist.append(threadName.get())
                            miniSaveList[:] = []
                            miniSaveList.append('H-link')
                            miniSaveList.append(link.get())
                            miniSaveList.append(baseLink.get())
                            miniSaveList.append(Gspan.get())
                            miniSaveList.append(Gclass.get())
                            miniSaveList.append(Gname.get())
                            miniSaveList.append(proxy.get())
                            miniSaveList.append(timeout.get())
                            miniSaveList.append(keyword.get())
                            miniSaveList.append(checkRedirect())
                            miniSaveList.append(threadName.get())
                            saveIndexList.append(miniSaveList)

                    else :
                            tkMessageBox.showinfo( "Error!", 'Not all values were filled out correctly!')

            elif option == 'Monitor HTML':

                    if ((link.get() and Gspan.get() and Gclass.get() and Gname.get() and threadName.get()) != '') == True  :
                            T = Thread(target = itemFunct, args = (link.get(), Gspan.get(), Gclass.get(), Gname.get(), proxy.get(), timeout.get(), checkRedirect(), threadName.get()))
                            T.start()
                            Tlist.append(threadName.get())
                            miniSaveList[:] = []
                            miniSaveList.append('Monitor HTML')
                            miniSaveList.append(link.get())
                            miniSaveList.append(Gspan.get())
                            miniSaveList.append(Gclass.get())
                            miniSaveList.append(Gname.get())
                            miniSaveList.append(proxy.get())
                            miniSaveList.append(timeout.get())
                            miniSaveList.append(keyword.get())
                            miniSaveList.append(checkRedirect())
                            miniSaveList.append(threadName.get())
                            saveIndexList.append(miniSaveList)  

                    else :
                            tkMessageBox.showinfo( "Error!", 'Not all values were filled out correctly!')

            elif option == 'Status Code':

                    if ((link.get() and threadName.get()) != '') == True  :
                            T = Thread(target = codeFunct, args = (link.get(), proxy.get(), timeout.get(), checkRedirect(), threadName.get()))
                            T.start()
                            Tlist.append(threadName.get())
                            miniSaveList[:] = []
                            miniSaveList.append('Status Code')
                            miniSaveList.append(link.get())
                            miniSaveList.append(proxy.get())
                            miniSaveList.append(timeout.get())
                            miniSaveList.append(checkRedirect())
                            miniSaveList.append(threadName.get())
                            saveIndexList.append(miniSaveList)

                    else :
                            tkMessageBox.showinfo( "Error!", 'Not all values were filled out correctly!')

            elif option == 'Shopify sitemap':

                    if ((link.get() and threadName.get()) != '') == True  :
                            T = Thread(target = ShofSitemapFunct, args = (link.get(), proxy.get(), timeout.get(), keyword.get(), threadName.get()))
                            T.start()
                            Tlist.append(threadName.get())
                            miniSaveList[:] = []
                            miniSaveList.append('link')
                            miniSaveList.append(link.get())
                            miniSaveList.append(proxy.get())
                            miniSaveList.append(timeout.get())
                            miniSaveList.append(keyword.get())
                            miniSaveList.append(threadName.get())
                            saveIndexList.append(miniSaveList)
                    else :
                            tkMessageBox.showinfo( "Error!", 'Not all values were filled out correctly!')

            elif option == 'Shopify restock':

                    if ((link.get() and threadName.get()) != '') == True  :
                            T = Thread(target = ShofRestockFunct, args = (link.get(), proxy.get(), timeout.get(), threadName.get()))
                            T.start()
                            Tlist.append(threadName.get())
                            miniSaveList[:] = []
                            miniSaveList.append('Shopify restock')
                            miniSaveList.append(link.get())
                            miniSaveList.append(proxy.get())
                            miniSaveList.append(timeout.get())
                            miniSaveList.append(threadName.get())
                            saveIndexList.append(miniSaveList)
                    else :
                            tkMessageBox.showinfo( "Error!", 'Not all values were filled out correctly!')

            elif option == 'Supreme restock':

                    if ((link.get() and threadName.get()) != '') == True  :
                            T = Thread(target = supRestockFunct, args = (link.get(), proxy.get(), timeout.get(), threadName.get()))
                            T.start()
                            Tlist.append(threadName.get())
                            miniSaveList[:] = []
                            miniSaveList.append('Supreme restock')
                            miniSaveList.append(link.get())
                            miniSaveList.append(proxy.get())
                            miniSaveList.append(timeout.get())
                            miniSaveList.append(threadName.get())
                            saveIndexList.append(miniSaveList)
                    else :
                            tkMessageBox.showinfo( "Error!", 'Not all values were filled out correctly!')

            else :
                    tkMessageBox.showinfo( "Error!", 'Unknown error!')
        else :
            tkMessageBox.showinfo( "Error!", 'This name has already been used!')


def checkRedirect():
    if redirectVar.get() == 1 :
        return True
    else :
        return False

def shade(option):

        if option == 'Link':
                baseLink.configure(state = 'normal')
                Gspan.configure(state = 'normal')
                Gclass.configure(state = 'normal')
                Gname.configure(state = 'normal')
                keyword.configure(state = 'normal')


        elif option == 'A-link':
                baseLink.configure(state = 'normal')
                Gspan.configure(state = 'disabled')
                Gclass.configure(state = 'disabled')
                Gname.configure(state = 'disabled')
                keyword.configure(state = 'normal')

        elif option == 'H-link':
                baseLink.configure(state = 'normal')
                Gspan.configure(state = 'normal')
                Gclass.configure(state = 'normal')
                Gname.configure(state = 'normal')
                keyword.configure(state = 'normal')

        elif option == 'Status Code':
                baseLink.configure(state = 'disabled')
                Gspan.configure(state = 'disabled')
                Gclass.configure(state = 'disabled')
                Gname.configure(state = 'disabled')
                keyword.configure(state = 'disabled')


        elif option == 'Monitor HTML':
                baseLink.configure(state = 'disabled')
                Gspan.configure(state = 'normal')
                Gclass.configure(state = 'normal')
                Gname.configure(state = 'normal')
                keyword.configure(state = 'disabled')

        elif option == 'Shopify sitemap':
                baseLink.configure(state = 'disabled')
                Gspan.configure(state = 'disabled')
                Gclass.configure(state = 'disabled')
                Gname.configure(state = 'disabled')
                keyword.configure(state = 'normal')

        elif option == 'Shopify restock':
                baseLink.configure(state = 'disabled')
                Gspan.configure(state = 'disabled')
                Gclass.configure(state = 'disabled')
                Gname.configure(state = 'disabled')
                keyword.configure(state = 'disabled')

        elif option == 'Supreme restock':
                baseLink.configure(state = 'disabled')
                Gspan.configure(state = 'disabled')
                Gclass.configure(state = 'disabled')
                Gname.configure(state = 'disabled')
                keyword.configure(state = 'disabled')

        else :
                tkMessageBox.showinfo( "Error!", 'Something went wrong, try again.')




####################################################################################################################################################################################################################


####################################################################################################################################################################################################################



app = Tk()
app.title('Page Phantom release 1.0')
w = 645 
h = 480 


ws = app.winfo_screenwidth() 
hs = app.winfo_screenheight() 

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

app.geometry('%dx%d+%d+%d' % (w, h, x, y))

app.configure(background='black')

####################################################################################################################################################################################################################

mb = StringVar(app)
mb.set('Link')
options = []
w = OptionMenu(app, mb, 'Link', 'A-link', 'H-link', "Status Code", 'Monitor HTML', 'Shopify sitemap', 'Shopify restock', 'Supreme restock', command = shade)
w.configure(bg = 'black')
w.place(x = 25, y = 25)


menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Import", command = importThreads)
filemenu.add_command(label="Export", command = csvWrite)
filemenu.add_command(label="Add Twitter auth", command = addTweeAuth)
filemenu.add_command(label="Auth Twitter", command = tweeLogin)
filemenu.add_separator()
menubar.add_cascade(label="File", menu=filemenu)
app.config(menu=menubar)

####################################################################################################################################################################################################################

linkl = Label(app, text = 'Link', background = 'black', fg = 'white')
linkl.place(x = 25, y = 65)
link = Entry(app, bd = 0, width = 60, background = 'white')
link.place(x = 70, y = 65)


baseLinkl = Label(app, text = 'Base Link', background = 'black', fg = 'white')
baseLinkl.place(x = 25, y = 100)
baseLink = Entry(app, bd = 0, width = 20, background = 'white')
baseLink.place(x = 100, y = 100)

threadNamel = Label(app, text = 'Thread Name', background = 'black', fg = 'white')
threadNamel.place(x = 305, y = 100)
threadName = Entry(app, bd = 0, width = 23, background = 'white')
threadName.place(x = 403, y = 100)

spanl = Label(app, text = 'Span', background = 'black', fg = 'white')
spanl.place(x = 25, y = 135)
Gspan = Entry(app, bd = 0, width = 10, background = 'white')
Gspan.place(x = 70, y = 135)

classl = Label(app, text = 'Class', background = 'black', fg = 'white')
classl.place(x = 185, y = 135)
Gclass = Entry(app, bd = 0, width = 10, background = 'white')
Gclass.place(x = 232, y = 135)

namel = Label(app, text = 'Name', background = 'black', fg = 'white')
namel.place(x = 352, y = 135)
Gname = Entry(app, bd = 0, width = 23, background = 'white')
Gname.place(x = 403, y = 135)

proxyl = Label(app, text = 'Proxy', background = 'black', fg = 'white')
proxyl.place(x = 25, y = 170)
proxy = Entry(app, bd = 0, width = 26, background = 'white')
proxy.place(x = 68, y = 170)

keywordl = Label(app, text = 'Keyword', background = 'black', fg = 'white')
keywordl.place(x = 335, y = 170)
keyword = Entry(app, bd = 0, width = 23, background = 'white')
keyword.place(x = 403, y = 170)

btn = Tkinter.Button(text = 'ADD', bd = 0, highlightbackground = 'black', fg = 'white', height = 1, width = 6, command = pickFunct)
btn.place(x = 260, y = 215)


timeoutl = Label(app, text = 'Timeout', background = 'black', fg = 'white')
timeoutl.place(x = 125, y = 30)
timeout = Entry(app, bd = 0, width = 4, background = 'white')
timeout.place(x = 190, y = 30)

redirectVar = IntVar()
redirect = Checkbutton(app, onvalue = 1, offvalue = 0,  selectcolor= 'blue', background = 'black')
redirect.place(x=370, y=30)
redirectl = Label(app, text = 'Allow redirects', background = 'black', fg = 'white')
redirectl.place(x = 265, y = 30)


stopBtn = Tkinter.Button(text = 'Stop thread', bd = 0, highlightbackground = 'black', fg = 'white', height = 1, width = 20, command = stopNameWin)
stopBtn.place(x = 413, y = 27)

consoleLog = ScrolledText(app, width = 84, height = 13)
consoleLog.place(x = 25, y = 265)



TlogWrite(consoleLog, ('Monitor application opened'))

####################################################################################################################################################################################################################

app.mainloop()






















