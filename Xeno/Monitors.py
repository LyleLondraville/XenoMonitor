import json
import time
import tweepy
import requests
from io import StringIO
from lxml.html import parse
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from Master import MisilaniousFunctions, SendFunctions, writeFunctions, RequestFunctions


class WebsiteScrapers(MisilaniousFunctions, SendFunctions, writeFunctions, RequestFunctions):
    
    def __init__(self):

        self.keyList = [ \
            ['Zc5PFiA8sUx6L8apImxsbihst', 'byAjv8wTXHqBpcydOY3jj2wynXlpTjPbsprJwQ2BD2359YjtGW','778351524313440256-9dEXC0Jsn02zCO3plAGhaUPsAqt7vbW', '5oSttpbCT13wN8nQDpaRwBSLj230mId0nsKeX3UrTn3Tv'], \
            ['iYjnidA3Cm0z6kH7xGRhAuzvT', 'd7JAEsqXkqFrj3xyN8M2ClXQfJEUSXPuGRfHB1tlKT3O4nQQp4','778351524313440256-upM4gQoZ06ChW906aEFvHGWHfoVLxFI', 'NmQTRsGVGnwVARULifpIYAuwnnJN0NJvVktw4mdDvddYV'], \
            ['8EkCLapfEbP83Vb6Z9qJgGgS8', 'a2blIN5cXt9MA5RjDPdtihLKN58JHZoWwouJBTjugFfQdoWZrX','778351524313440256-0A34QW5djunbuUS9ijnD2tjtKY9Ostx', 'uIT4mN6AT3LPskZMFTsak9Wz4ziGxhGe6b3WS9E7ffvYh'], \
            ['RNQ7e0Vr1p590p3Br7kP9snhP', 'fJjxjFoUM0TAwh4whD2rZjPwz2hBm1j4XhVQXqZ5QTvPgTopOO','778351524313440256-aPVcYcz8ewik8G3H51PwXKkDrz16AXY', 'pRkg18Jkd94PWwSOCVW5w4otKQJ4mcgYvBlvkjeojumWJ']]

        self.keyIndex = 0
        self.sentlinks = []
        self.savedImages = []
        self.startTime = time.time()

        authList = self.keyList[self.keyIndex]

        auth = tweepy.OAuthHandler(authList[0], authList[1])
        auth.set_access_token(authList[2], authList[3])

        self.api = tweepy.API(auth) 
    
    def imageLxml(self, url, selector, textSelect, imageSelector, headers, timeout, name):

        self.writeFile(name)
        count = 0
        sess = requests.Session()
        fileName =  '{}.out'.format(name.replace(' ', '-'))
        
        initalTime = time.time()
        original = []
        dashCount = 0

        for i in range(0, len(url)):
            if url[i] == '/':
                if dashCount == 2:
                    baseurl = url[0:i+1]
                    imageBaseurl = url[0:i]
                    break
                else :
                    dashCount += 1

        cntnt = self.getRequ(sess, url, headers,  name)
        doc = parse(StringIO(cntnt.text)).getroot()

        cLink = doc.cssselect(selector)
        cText = (doc.cssselect(textSelect) if textSelect != '' else range(0, len(cLink)))
        cImage = doc.cssselect(imageSelector) if imageSelector != '' else range(0, len(cLink))

        
        if baseurl.replace('http://', '').replace('https://', '').replace('www.', '') in cLink[0].get('href'):
            baseurl = ''
        else :
            baseurl = (baseurl[0:len(baseurl)-1] if cLink[0].get('href')[0] == '/' else baseurl)


        if type(cImage[0]) != int :
        
            tempImage = cImage[0].get('src')

            if tempImage[0:2] == '//' :
                imageIndex = 2
                imageBaseurl = ''
                print ( '{} image - {}'.format(name, cImage[0].get('src')[imageIndex:]))
            
            elif tempImage[0:2] == '..' :
                imageIndex = 0
                imageBaseurl += '/shop'
                baseurl += '/shop'
                print ( '{} image - {}{}'.format(name, imageBaseurl, cImage[0].get('src').replace('..', '')))
            
            else :
                imageIndex = 0
                imageBaseurl = (imageBaseurl if tempImage[0:1] == '/' else '')

                print ( '{} image - {}{}'.format(name, imageBaseurl, cImage[0].get('src')))

        else :
            print ('{} image - Null image'.format(name))
            imageBaseurl = ''
            imageIndex = '' 

        for l in cLink:
            link = l.get('href')
            original.append(link)

        print ( '{} link - {}{}'.format(name, baseurl, cLink[0].get('href').replace('..', '')))

        try :
            print ( '{} text - {}'.format( name, (self.normalizeText(cText[0].text_content()) if type(cText[0]) != int else "Null text")))
        except :
            print ( '{} text - shit idk'.format(name))

        while True:

            '''
            if refTimeout != 0:
                if time.time() - initalTime >= 60*60*refTimeout :

                    original[:] = []

                    cntnt = self.getRequ(sess, url, headers, name)
                    doc = parse(StringIO(cntnt.text)).getroot()

                    for l in doc.cssselect(selector):
                        original.append( l.get('href') )

                    initalTime = time.time()

                else :
                    pass
            else :
                pass
            '''

            doc = None
            cntnt = None
            cLink = None
            cText = None
            cImage = None

            t1 = time.time()

            time.sleep(timeout)

            cntnt = self.getRequ(sess, url, headers, name)

            doc = parse(StringIO(cntnt.text)).getroot()

            cLink = doc.cssselect(selector)
            cText = doc.cssselect(textSelect) if textSelect != '' else range(0, len(cLink))
            cImage = doc.cssselect(imageSelector) if imageSelector != '' else range(0, len(cLink))
            
            for l, t, i in zip( cLink , cText, cImage):

                link = l.get('href')

                if link not in original:

                    text = (self.normalizeText(t.text_content()) if type(t) != int else 'Null Product Title')
                    image = (i.get('src') if type(i) != int else 'Null')

                    if self.filter('{}{}{}'.format(text.lower(), link, image)) == True:
                        sendLink = '{}{}'.format(baseurl, link.replace('..', ''))
                        sendImg = '{}{}'.format(imageBaseurl, image[imageIndex:].replace('..', ''))
                        self.tweetImageData( '{}\n{}'.format( text, sendLink ), sendImg )
                        self.appendTxt(fileName, 'Sent at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), link, text, image))


                    else :
                        #self.tellegramMessage('{}\n{}{}'.format( text, baseurl, link ))
                        self.appendTxt(fileName, 'Found at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), link, text, image))

                    original.append(link)

            count += 1

            self.writeUpdate(0, name, len(original), cntnt.status_code, round((time.time()-t1), 2), count)
            
    def lxmlNeverTweetSameThing(self, baseurl, url, linkPreSelect, linkSelect, linkSelectOption, textPreselect, textSelect, imagePreSelect, imageSelect, imageOption, imgBaseURL, imageIndex, headers, timeout, name):

        self.writeFile(name)
        count = 0
        fileName = '{}.out'.format(name.replace(' ', ''))
        sess = requests.Session()

        links = ['Null']
        images = []
        texts = []

        cntnt = self.getRequ(sess, url, headers,  name)
        doc = parse(StringIO(cntnt.text)).getroot()

        linkCSS  = doc.cssselect(linkPreSelect)
        textCSS  = (doc.cssselect(textPreselect) if textPreselect != '' else range(0, len(linkCSS)))
        imageCSS = (doc.cssselect(imagePreSelect) if imagePreSelect != '' else range(0, len(linkCSS)))

        for l, t, i in zip(linkCSS, textCSS, imageCSS):
            try :
                linkHTML = l.cssselect(linkSelect)[0]
                productLink = baseurl + str(linkHTML.get(linkSelectOption))
            except :
                print ('{} - error loading link'.format(name))
                productLink = 'Null'
            
            try :
                textHTMl = t.cssselect(textSelect)[0]
                productText = (self.normalizeText(textHTMl.text_content())  if type(t) != int else 'Null')
            except:
                print ('{} - error loading text'.format(name))
                if productLink == 'Null':
                    productText = 'Null'
                else :
                    productText = self.parseName(productLink)
            
            try :
                imageHTMl = i.cssselect(imageSelect)[0]
                productImage = (imgBaseURL + imageHTMl.get(imageOption)[imageIndex:] if type(i) != int else 'Null')
            except:
                print ('{} - error loading image'.format(name))
                productImage = 'Null'

            links.append(productLink)
            images.append(productImage)
            texts.append(productText)         

        print ('link - {}\nText - {}\nImage - {}'.format(links[1], texts[0], images[0]))

        while True:

            t1 = time.time()
            time.sleep(timeout)

            cntnt = self.getRequ(sess, url, headers,  name)
            doc = parse(StringIO(cntnt.text)).getroot()
                
            linkCSS  = doc.cssselect(linkPreSelect)
            textCSS  = (doc.cssselect(textPreselect) if textPreselect != '' else range(0, len(linkCSS)))
            imageCSS = (doc.cssselect(imagePreSelect) if imagePreSelect != '' else range(0, len(linkCSS)))

            for l, t, i in zip(linkCSS, textCSS, imageCSS):
                try :
                    linkHTML = l.cssselect(linkSelect)[0]
                    productLink = baseurl + str(linkHTML.get(linkSelectOption))
                except :
                    productLink = 'Null'
                
                try :
                    textHTMl = t.cssselect(textSelect)[0]
                    productText = (self.normalizeText(textHTMl.text_content())  if type(t) != int else 'Null')
                except:
                    if productLink == 'Null':
                        productText = 'Null'
                    else :
                        productText = self.parseName(productLink)
                
                try :
                    imageHTMl = i.cssselect(imageSelect)[0]
                    productImage = (imgBaseURL + imageHTMl.get(imageOption)[imageIndex:] if type(i) != int else 'Null')
                except:
                    productImage = 'Null'


                if (productLink not in links) and (productImage not in images) and (productText not in texts):
                    if self.filter('{}{}{}'.format(productLink, productText, productImage)) == True :
                        self.tweetImageData('{}\n{}'.format(productText, productLink), productImage)
                        self.appendTxt(fileName, 'Sent at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, productText, productImage))

                    else :
                        #self.tellegramMessage('{}\n{}'.format(productLink, productText))
                        self.appendTxt(fileName, 'Found at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, productText, productImage))

                    links.append(productLink)
                    texts.append(productText)
                    
                    if productImage == 'Null':
                        pass
                    else :
                        images.append(productImage)

            count += 1
            self.writeUpdate(0, name, len(links), cntnt.status_code, round((time.time()-t1), 2), count)
              
    def superSelector(self, baseurl, url, linkPreSelect, linkSelect, linkSelectOption, textPreselect, textSelect, imagePreSelect, imageSelect, imageOption, imgBaseURL, imageIndex, headers, timeout, name):
        
        self.writeFile(name)
        count = 0
        fileName = '{}.out'.format(name.replace(' ', ''))
        sess = requests.Session()
        
        links = [None]
        images = []
        texts = []

        initalTime = time.time()

        cntnt = self.getRequ(sess, url, headers,  name)
        doc = parse(StringIO(cntnt.text)).getroot()

        linkCSS  = doc.cssselect(linkPreSelect)
        textCSS  = (doc.cssselect(textPreselect) if textPreselect != None else range(0, len(linkCSS)))
        imageCSS = (doc.cssselect(imagePreSelect) if imagePreSelect != None else range(0, len(linkCSS)))


        for l, t, i in zip(linkCSS, textCSS, imageCSS):
            try :
                linkHTML = l.cssselect(linkSelect)[0]
                productLink = baseurl + str(linkHTML.get(linkSelectOption))
            except :
                print ('{} - error loading link'.format(name))
                productLink = None
            
            textHTMl = (t.cssselect(textSelect)[0] if type(t) != int else None)
            productText = (self.normalizeText(textHTMl.text_content())  if type(t) != int else None)
            try :
                imageHTMl = i.cssselect(imageSelect)[0]
                productImage = (imgBaseURL + imageHTMl.get(imageOption)[imageIndex:] if type(i) != int else None)
            except:
                print ('{} - error loading image'.format(name))
                productImage = None

            links.append(productLink)
            images.append(productImage)
            texts.append(productText)

        print (links)

        
        print ('link - {}\nText - {}\nImage - {}'.format(links[1], texts[0], images[0]  ))
         
        while True:

            t1 = time.time()

            time.sleep(timeout)

            cntnt = self.getRequ(sess, url, headers, name)
            doc = parse(StringIO(cntnt.text)).getroot()
            
            linkCSS  = doc.cssselect(linkPreSelect)
            textCSS  = (doc.cssselect(textPreselect) if textPreselect != '' else range(0, len(linkCSS)))
            imageCSS = (doc.cssselect(imagePreSelect) if imagePreSelect != '' else range(0, len(linkCSS)))

            for l, t, i in zip(linkCSS, textCSS, imageCSS):
                try :
                    linkHTML = l.cssselect(linkSelect)[0]
                    productLink = baseurl + str(linkHTML.get(linkSelectOption))
                except :
                    productLink = 'Null'
                
                try :
                    textHTMl = t.cssselect(textSelect)[0]
                    productText = (self.normalizeText(textHTMl.text_content())  if type(t) != int else 'Null')
                except:
                    if productLink == 'Null':
                        productText = 'Null'
                    else :
                        productText = self.parseName(productLink)
                
                try :
                    imageHTMl = i.cssselect(imageSelect)[0]
                    productImage = (imgBaseURL + imageHTMl.get(imageOption)[imageIndex:] if type(i) != int else 'Null')
                except:
                    productImage = 'Null'

                if productLink not in links :    
                    
                    if self.filter( '{}{}{}'.format(productLink, productText, productImage) ) == True:
                        self.tweetImageData( '{}\n{}'.format(productLink, productText), productImage )
                        self.appendTxt(fileName, 'Sent at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, productText, productImage))

                    else :
                        self.appendTxt(fileName, 'Found at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, productText, productImage))

                    links.append(productLink)

            count += 1
            self.writeUpdate(0, name, len(links), cntnt.status_code, round((time.time()-t1), 2), count )

    def headlessScrape(self, baseurl, url, linkPreSelect, linkSelect, linkSelectOption, textPreselect, textSelect, imagePreSelect, imageSelect, imageOption, imgBaseURL, imageIndex, timeout, name):

        try :
            self.writeFile(name)
            count = 0
            fileName = '{}.out'.format(name.replace(' ', ''))

            links = [None]
            images = []
            texts = []

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
            chrome_options.add_argument(f'user-agent={user_agent}')
            print ("{} : {} Starting Chrome driver....".format(self.t(), name))
            driver = webdriver.Chrome('/Users/lylelondraville/Desktop/Python Scripts/Page Monitor/Xeno/chromedriver',chrome_options=chrome_options)
            print ("{} : {} Chrome driver started, loading page.....".format(self.t(), name))

            driver.get(url)


            initalTime = time.time()

            doc = parse(StringIO(driver.page_source)).getroot()

            linkCSS  = doc.cssselect(linkPreSelect)
            textCSS  = (doc.cssselect(textPreselect) if textPreselect != None else range(0, len(linkCSS)))
            imageCSS = (doc.cssselect(imagePreSelect) if imagePreSelect != None else range(0, len(linkCSS)))


            for l, t, i in zip(linkCSS, textCSS, imageCSS):
                try :
                    linkHTML = l.cssselect(linkSelect)[0]
                    productLink = baseurl + str(linkHTML.get(linkSelectOption))
                except :
                    print ('{} - error loading link'.format(name))
                    productLink = None

                textHTMl = (t.cssselect(textSelect)[0] if type(t) != int else None)
                productText = (textHTMl.text_content().replace('\n', '').replace('\t', '').replace('  ', '')  if type(t) != int else None)

                try :
                    imageHTMl = i.cssselect(imageSelect)[0]
                    productImage = (imgBaseURL + imageHTMl.get(imageOption)[imageIndex:] if type(i) != int else None)
                except:
                    print ('{} - error loading image'.format(name))
                    productImage = None

                links.append(productLink)
                images.append(productImage)
                texts.append(productText)


            print ('link - {}\nText - {}\nImage - {}'.format(links[1], texts[0], images[0]  ))

            while True:

                t1 = time.time()

                time.sleep(timeout)

                driver.refresh()
                doc = parse(StringIO(driver.page_source)).getroot()

                linkCSS  = doc.cssselect(linkPreSelect)
                textCSS  = (doc.cssselect(textPreselect) if textPreselect != None else range(0, len(linkCSS)))
                imageCSS = (doc.cssselect(imagePreSelect) if imagePreSelect != None else range(0, len(linkCSS)))

                for l, t, i in zip(linkCSS, textCSS, imageCSS):
                    try :
                        linkHTML = l.cssselect(linkSelect)[0]
                        productLink = baseurl + str(linkHTML.get(linkSelectOption))
                    except :
                        productLink = None

                    try :
                        textHTMl = t.cssselect(textSelect)[0]
                        productText = (textHTMl.text_content().replace('\n', '').replace('\t', '').replace('  ', '')  if type(t) != int else None)
                    except:
                        if productLink == None:
                            productText = None
                        else :
                            productText = self.parseName(productLink)

                    try :
                        imageHTMl = i.cssselect(imageSelect)[0]
                        productImage = (imgBaseURL + imageHTMl.get(imageOption)[imageIndex:] if type(i) != int else None)
                    except:
                        productImage = None

                    if productLink not in links :

                        if self.filter( '{}{}{}'.format(productLink, productText, productImage) ) == True:
                            self.tweetImageData( '{}\n{}'.format(productLink, productText), productImage )
                            self.appendTxt(fileName, 'Sent at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, productText, productImage))

                        else :
                            self.appendTxt(fileName, 'Found at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, productText, productImage))

                        links.append(productLink)

                count += 1
                self.writeUpdate(0, name, len(links), "NULL STATUS CODE", round((time.time()-t1), 2), count )

        except Exception as e:
            self.tellegramMessage("{} - {} ERROR\n\n\n{}".format(self.t(), name, e))

    def basicSitemap(self, url, headers, timeout, name):

        self.writeFile(name)
        count = 0
        sess = requests.Session()

        original = []
        initalTime = time.time()

        etreeFromstring = ET.fromstring
        #getChildren = sitemap.getchildren
        
        cntnt = self.getRequ(sess, url, headers, name)
        root = etreeFromstring(cntnt.content)
            
        for sitemap in root:
            child = sitemap.getchildren()
            original.append(child[0].text)

        while True:

            t1 = time.time()

            time.sleep(timeout)

            '''
            if refTimeout != 0:
                if time.time() - initalTime >= 60*60*refTimeout :

                    original[:] = []

                    cntnt = self.getRequ(sess, url, headers, name)
                    root = etreeFromstring(cntnt.content)
                        
                    for sitemap in root:
                        child = sitemap.getchildren()
                        original.append(child[0].text)

                    initalTime = time.time()
                else :
                    pass
            else :
                pass
            '''

            cntnt = self.getRequ(sess, url, headers, name)

            try :
                root = etreeFromstring(cntnt.content)
                passed = True 
            except :
                passed = False 
            
            if passed == True :
                
                for sitemap in root:
                    child = sitemap.getchildren()
                    link = child[0].text
                    
                    if link not in original:
                        message = '{}\n{}'.format( self.parseName(link), link )
                        
                        if self.filter(message) == True:
                            self.tweetRegular( message )
                        
                        original.append(link)

                count += 1
                self.writeUpdate(0, name, len(original), cntnt.status_code, round((time.time()-t1), 2), count)
            
            else :
                print ( ('[{}] : {} - error loading lxml').format( self.t(), name ) )
    
    def sivasSpecific(self):
        
        self.writeFile('Sivas')
        count = 0
        sess = requests.Session()
        
        links = []
        images = []
        texts = []

        initalTime = time.time()

        cntnt = self.getRequ(sess, 'https://www.sivasdescalzo.com/en/lifestyle/sneakers', {},  'Sivas')
        doc = parse(StringIO(cntnt.text)).getroot()

        for css in doc.cssselect('div.product'):
            productLink = css.cssselect('a')[2].get('href')
            text = self.parseName(productLink)
            image = css.cssselect('a img')[1].get('src')

            links.append(productLink)
            images.append(image)
            texts.append(text)  
        

        print ('link - {}\nText - {}\nImage - {}'.format(links[0], texts[0], images[0]))
        
        while True:


            if time.time() - initalTime >= 60*60*24 :

                links[:] = []

                cntnt = self.getRequ(sess, 'https://www.sivasdescalzo.com/en/lifestyle/sneakers', {},  'Sivas')
                doc = parse(StringIO(cntnt.text)).getroot()

                for css in doc.cssselect('div.product'):
                    productLink = css.cssselect('a')[2].get('href')
                    text = self.parseName(productLink)
                    image = css.cssselect('a img')[1].get('src')

                    links.append(productLink)
                    images.append(image)
                    texts.append(text) 
                
                initalTime = time.time()

            else :
                pass



            t1 = time.time()

            time.sleep(4)

            cntnt = self.getRequ(sess, 'https://www.sivasdescalzo.com/en/lifestyle/sneakers', {},  'Sivas')
            doc = parse(StringIO(cntnt.text)).getroot()

            for css in doc.cssselect('div.product'):
                productLink = css.cssselect('a')[2].get('href')
                text = self.parseName(productLink)
                image = css.cssselect('a img')[1].get('src')

                if productLink not in links :    
                    if self.filter( '{}{}{}'.format(productLink, text, image) ) == True:
                        self.tweetImageData( '{}\n{}'.format(productLink, text), image )
                        self.appendTxt('Sent at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, text, image), 'Sivas.out')

                    else :
                        self.appendTxt('Found at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, text, image), 'Sivas.out')

                    links.append(productLink)

            count += 1
            self.writeUpdate(0, 'Sivas', len(links), cntnt.status_code, round((time.time()-t1), 2), count)

    def mrPorter(self):


        url = 'https://api.net-a-porter.com/MRP/US/en/60/0/summaries?categoryIds=4140&onSale=false&sort=new-in'

        self.writeFile("MR PORTER")

        originalProducts = []
        foundProducts = []
        newProducts = []
        load = json.loads
        dump = json.dumps
        count = 0

        s = requests.Session()
        r = self.simpleGetReq(s, url, {}, "MR PORTER")
        products = load(r.text)['summaries']

        for p in products:
            productJson = load(dump(p))
            pid = str(productJson['id'])
            originalProducts.append(pid)


        while True:

            time.sleep(1)
            t1 = time.time()


            r = self.simpleGetReq(s, url, {}, "MR PORTER")


            if r.status_code == 200:
                count += 1
                products = load(r.text)['summaries']

                for p in products:
                    productJson = load(dump(p))

                    pid = str(productJson['id'])

                    if pid not in originalProducts:
                        newProducts.append(pid)

                    else :
                        foundProducts.append(pid)


                originalProducts[:] = list(set(originalProducts) - (set(originalProducts) - set(foundProducts)))

                for i in newProducts:
                    originalProducts.append(i)
                    r = self.simpleGetReq(s, 'https://api.net-a-porter.com/MRP/US/en/detail/{}'.format(i), {}, "MR PORTER" )
                    jsonData = load(r.text)

                    name = jsonData['analyticsKey'].replace(' ', '-')
                    brand = load(dump(jsonData['brand']))['name']

                    productURL = 'https://www.mrporter.com/en-us/mens/{}/{}/{}'.format(brand.replace(' ', '_'), name.replace('+', '-'), i)
                    imageURL = 'https://cache.mrporter.com/images/products/{}/{}_mrp_fr_l.jpg'.format(i, i)

                    self.tweetImageData('{}\n{}'.format( '{} {}'.format(brand, name), productURL), imageURL)
            else :
                print ("Get err")
                time.sleep(5)

            self.writeUpdate(0, "MR PORTER", len(originalProducts), r.status_code, round((time.time() - t1), 2), count)

    def footpatrol(self):

        try :

            self.writeFile("Footpatrol")
            fileName = '{}.out'.format("Footpatrol")

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
            chrome_options.add_argument(f'user-agent={user_agent}')
            print ("{} : {} Starting Chrome driver....".format(self.t(), "Footpatrol"))
            driver = webdriver.Chrome('/Users/lylelondraville/Desktop/Python Scripts/Page Monitor/Xeno/chromedriver',chrome_options=chrome_options)
            print ("{} : {} Chrome driver started, loading page.....".format(self.t(), "Footpatrol"))

            driver.get("https://www.footpatrol.com/footwear/latest-footwear/")

            self.getSeleniumMesh(driver)

            links = []
            images = []
            texts = []
            count = 0


            doc = parse(StringIO(driver.page_source)).getroot()


            for l, t, i in zip(doc.cssselect("div.fp-product-thumb a"), doc.cssselect("h4.fp-product-thumb-title"), doc.cssselect("div.fp-product-thumb img")):

                links.append("https://www.footpatrol.com{}".format(l.get("href")))
                texts.append(t.text_content().replace('\n', '').replace('\t', '').replace('  ', ''))
                images.append(i.get("src"))


            print ('link - {}\nText - {}\nImage - {}'.format(links[0], texts[0], images[0]))

            while True:

                t1 = time.time()
                time.sleep(3)

                self.getSeleniumMesh(driver)
                doc = parse(StringIO(driver.page_source)).getroot()

                for l, t, i in zip(doc.cssselect("div.fp-product-thumb a"), doc.cssselect("h4.fp-product-thumb-title"), doc.cssselect("div.fp-product-thumb img")):

                    productLink = "https://www.footpatrol.com{}".format(l.get("href"))
                    productText = self.normalizeText(t.text_content())
                    productImage = i.get('img')

                    if (productLink not in links):
                        if self.filter('{}{}{}'.format(productLink, productText, productImage)) == True :
                            self.tweetImageData('{}\n{}'.format(productText, productLink), productImage)
                            self.appendTxt(fileName, 'Sent at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, productText, productImage))

                        else :
                            self.appendTxt(fileName, 'Found at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, productText, productImage))

                        links.append(productLink)
                        texts.append(productText)
                        images.append(productImage)

                count += 1
                self.writeUpdate(0, "Footpatrol", len(links), "NULL STATUS CODE", round((time.time()-t1), 2), count)


        except Exception as e:
            self.tellegramMessage("Footpatrol error encountered at {}\n\n\n{}".format(self.t(), e))

    def DSMpoolScrape(self, pages, timeout):

        pageIndex = 0
        count = 0
        masterList = []

        for i in range(0, len(pages)):
            masterList.append([i])

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome('/Users/lylelondraville/Desktop/Python Scripts/Page Monitor/Xeno/chromedriver',chrome_options=chrome_options)

        for t in pages :
            links = []
            tabName  = 'tab{}'.format(pageIndex)
            self.writeFile(t.replace('https://shop.doverstreetmarket.com', '').replace('/', '-').replace('index', '')[1:])
            fileName = t.replace('https://shop.doverstreetmarket.com', '').replace('/', '-').replace('index', '')[1:]
            driver.execute_script("window.open('about:blank', '{}');".format(tabName))
            driver.switch_to.window(tabName)
            driver.get(t)

            doc = parse(StringIO(driver.page_source)).getroot()

            links.append(tabName)
            links.append(fileName)

            for l in doc.cssselect('li.item a'):
                tempLink = l.get('href')
                if tempLink not in links:
                    links.append(tempLink)

            masterList[pageIndex][:] = links

            links[:]=[]
            pageIndex += 1

        while True :

            for i in range(0, len(masterList)):

                tempList = masterList[i]

                count += 1
                time.sleep(timeout)
                t1 = time.time()

                name = tempList[0]
                fileName = tempList[1]

                driver.switch_to.window(name)
                driver.refresh()

                doc = parse(StringIO(driver.page_source)).getroot()

                for l, t, i in zip(doc.cssselect('li.item a'), doc.cssselect('h2.product-name'), doc.cssselect('a.product-image img')):

                    productLink = l.get('href')

                    if productLink not in tempList :

                        productText = t.text_content().replace('\n', '').replace('\t', '').replace('  ', '')
                        productImage = i.get('src')

                        if self.filter( '{}{}{}'.format(productLink, productText, productImage) ) == True:
                            self.tweetImageData( '{}\n{}'.format(productLink, productText), productImage )
                            self.appendTxt(fileName, 'Sent at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, productText, productImage))

                        else :
                            self.appendTxt(fileName, 'Found at {}\n\tlink - {}\n\ttext - {}\n\timage - {}'.format(self.t(), productLink, productText, productImage))

                        masterList[i].append(productLink)

                self.writeUpdate(0, fileName, len(masterList[i]), "NULL STATUS CODE", round((time.time()-t1), 2), count )

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

        oldCntnt  = self.getRequ(s, sitemapUrl, {}, name)
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

            newCntnt = self.getRequ(s, sitemapUrl, {}, name)

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




