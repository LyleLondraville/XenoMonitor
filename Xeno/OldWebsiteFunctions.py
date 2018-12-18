from threading import Thread
from multiprocessing import Process

from Monitors import TextLink
from Shopify import shopy

import requests

try :
    urllib3
    urllib3.disable_warnings()
except :
    pass

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class cook(TextLink, shopy):

    def test(self):

        leBuxHeaders = {
            'Host': 'www.lebuzzsneakershop.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
        }

        lableHeaders = {
            'Host': 'shop.labelsfashion.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
        }

        levelHeaders = {
            'Host': 'www.levelshoes.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
        }

        monarHeaders = {
            'Host': 'www.monar.be',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
        }

        loadedHeaders = {
            'Host': 'www.loadednz.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8'}

        footHeaders = {
            'Host': 'www.footpatrol.co.uk',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8'}

        sizeHeaders = {
            'Host': 'www.size.co.uk',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'en-US,en;q=0.8'}

        flannelsHeaders = {
            'Host': 'www.flannels.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8'}

        clickHeaders = {
            'Host': 'www.clickskicks.net',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
        }

        oneBlockHeaders = {
            'Host': 'www.oneblockdown.it',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9'}

        istmHeaders = {
            'Host': 'ist.290sqm.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8'}

        nighHeaders = {

            'Host':'www.nighshop.com',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'en-US,en;q=0.9',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

        pataHeaders = {
            'Host': 'www.patta.nl',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

        }

        #Process(target = self.imageLxml, args = ('https://www.barneys.com/category/men/shoes/sneakers/adidas/N-j68mm4Z11mt8ibZ1qejbtZ1jwafu9Z1u1y6z6Z14s5iuoZ7ewj0kZ14w3h1iZb1emo1ZukkbluZ14gyxplZm2idkaZ1jn0wd9?Ns=product.new%7C1%7C%7Cproduct.startDate%7C1&viewAll=true&viewAll=true&page=1', 'a.thumb-link', 'a.thumb-link img', 'div.wrap-desc', {}, 1,  24, 'Barneys')).start()


    def good(self):

        Process(target=self.mrPorter, args=()).start()
        Process(target=self.sivasSpecific, args=()).start()
        Process(target = self.lxmlNeverTweetSameThing, args = ('', 'https://www.solebox.com/en/Footwear/', 'li.productData', 'a.fn', 'href', 'li.productData', 'div.titleBlock', 'li.productData', 'div.gridPicture img', 'src', '', 0, {}, 1, 'solebox')).start()
        Process(target = self.lxmlNeverTweetSameThing, args = ('', 'https://www.allikestore.com/german/sneakers.html', 'div.item-wrap', 'a', 'href', 'h2.product-name', 'a', 'div.item-wrap', 'img', 'src', '', 0, {}, 1, 'Allike Store')).start()
        Process(target = self.superSelector, args = ('', 'https://www.vooberlin.com/men/footwear', 'div.product-item-info a', 'a', 'href', '', '', 'div.product-item-info', 'img', 'src', '', 0, {}, 1, 24, 'Vooberlin-women' )).start()
        Process(target = self.superSelector, args = ('http://runcolors.com', 'http://runcolors.com/snaekers.html', 'li.pList__item', 'a', 'href', 'li.pList__item', 'span.pList__title', '', 'img', 'src', 'http://runcolors.com/', 0, {}, 1, 24, 'runcolors')).start()
        Process(target = self.superSelector, args = ('http://www.numbersneakers.com/', 'http://www.numbersneakers.com/novedades-c102x2771877', 'div.PBItemImg', 'a', 'href', 'div.PBItemName', 'a', 'div.PBItemImg', 'img', 'src', 'http://www.numbersneakers.com/',0, {} , 1, 24, 'numbersneakers')).start()
        Process(target = self.superSelector, args = ('', 'http://www.novoidplus.com/shop/chaussures-c-28.html?page=1&sort=2', 'li.listingContainer', 'div.swap1 a', 'href', 'li.listingContainer', 'div.captsion', 'li.listingContainer', 'div.swap1 img', 'src', 'http://www.novoidplus.com/shop/', 0, {}, 1, 24, 'novoidplus')).start()
        Process(target = self.superSelector, args = ('https://www.bstnstore.com', 'https://www.bstnstore.com/en/footwear', 'li.item', 'a', 'href', 'div.pText', 'a', 'li.item', 'img', 'src', 'https://www.bstnstore.com', 0, {}, 1, 24, 'BSTN-store' )).start()
        Process(target = self.superSelector, args = ('', 'http://www.starcowparis.com/new-products', 'div.item', 'a', 'href', 'div.item', 'span.content', 'div.item', 'span.image img', 'src', '', 0, {}, 1, 24, 'Starcow Paris')).start()
        Process(target = self.superSelector, args = ('', 'http s://www.hit-the-spot.com/New-Arrivals/', 'li.productData', 'a.pictureProduct', 'href', 'li.productData', 'a.title', 'li.productData', 'a.pictureProduct img', 'data-lazy-src', '', 0, {}, 1, 24, 'Hit the Spot')).start()
        Process(target = self.superSelector, args = ('http://www.sneak-a-venue.com', 'http://www.sneak-a-venue.com/new', 'li.item', 'div.pImageContainer a', 'href', 'li.item', 'div.pText', 'li.item', 'a.plink img', 'src', 'http://www.sneak-a-venue.com', 0, {}, 1, 24, 'sneak a venue' )).start()
        Process(target = self.superSelector, args = ('https://www.43einhalb.com', 'https://www.43einhalb.com/en/new-arrivals', 'li.item', 'a', 'href', 'li.item', 'a.pName', 'li.item', 'img', 'data-src', '', 0, {}, 1, 24, '43einhalb-new' )).start()
        Process(target = self.superSelector, args = ('https://www.43einhalb.com', 'https://www.43einhalb.com/en/restock', 'li.item', 'a', 'href', 'li.item', 'a.pName', 'li.item', 'img', 'data-src', '', 0, {}, 1, 24, '43einhalb-restock' )).start()
        Process(target = self.superSelector, args = ('https://www.43einhalb.com', 'https://www.43einhalb.com/en/coming-soon', 'li.item', 'a', 'href', 'li.item', 'a.pName', 'li.item', 'img', 'data-src', '', 0, {}, 1, 24, '43einhalb-comingsoon' )).start()
        Process(target = self.superSelector, args = ('http://www.footish.se', 'http://www.footish.se/en/sneakers', 'div.product-image', 'a', 'href', 'div.product-name', 'h3', '', '', '', '', 0, {}, 1, 24, 'footish' )).start()
        Process(target = self.basicSitemap, args = ('http://www.lebuzzsneakershop.com/sitemap.xml', leBuxHeaders, 1, 24, 'lebuzzsneakershop')).start()
        Process(target = self.basicSitemap, args = ('https://shop.labelsfashion.com/sitemap.xml', lableHeaders, 1, 24, 'labelsfashion')).start()
        Process(target = self.basicSitemap, args = ('https://www.levelshoes.com/sitemap.xml', levelHeaders, 1, 24, 'levelshoes')).start()
        Process(target = self.basicSitemap, args = ('http://www.monar.be/sitemap.xml', monarHeaders, 1, 24, 'monar')).start()
        Process(target = self.basicSitemap, args = ('http://www.clickskicks.net/sitemap.xml', clickHeaders, 4, 24, 'clickskicks')).start()
        Process(target = self.basicSitemap, args = ('http://www.oneblockdown.it/sitemap.xml', oneBlockHeaders, 4, 24, 'oneblockdown')).start()
        Process(target = self.imageLxml, args = ('http://www.oqiumstore.com/men', 'a.lst-img', 'a.nom', 'a.lst-img img', {}, 1, 24, 'oqiumstore')).start()
        Process(target = self.imageLxml, args = ('https://www.suppastore.com/latest/', 'a.product-cover__link', 'div.product-cover__model', '', {}, 1, 24, 'Suppa store')).start()
        Process(target = self.imageLxml, args = ('https://reissue.nl/sneakers', 'div.caption a', 'div.caption h4', 'div.product-thumb img', {}, 1, 24, 'Reissue')).start()
        Process(target = self.imageLxml, args = ('http://nigramercato.com/t/calzado', 'a.product-name', 'a.product-name', 'div.inline img', {}, 1, 24, 'Nigramercato')).start()
        Process(target = self.imageLxml, args = ('https://www.ymeuniverse.com/en/sneakers', 'div.item-wrapper a', 'h2.product-name', 'span.product-image img', {}, 1, 24, 'YME universe')).start()
        Process(target = self.imageLxml, args = ('https://brandshop.ru/muzhskoe/obuv/', 'a.product-image', '', 'a.product-image img', {}, 1,  24, 'brandshop')).start()
        Process(target = self.imageLxml, args = ('http://www.inflammable.com/en/sneakers/', 'div.prliSpic a', 'div.prliStxt', 'div.prliSpic img', {}, 1, 24, 'inflammable')).start()
        Process(target = self.imageLxml, args = ('https://www.mrqt.net/latest/?p=1', 'div.product-cover a', 'div.product-cover__content-wrapper img', '', {}, 1,  24, 'mrqt')).start()
        Process(target = self.imageLxml, args = ('http://goodhoodstore.com/mens/all-mens-footwear', 'div.overview a', 'div.inner p', 'div.overview img', {}, 1, 24, 'goodhoodstore')).start()
        Process(target = self.imageLxml, args = ('https://footdistrict.com/zapatillas/novedades.html', 'h2.product-name a', 'h2.product-name', 'a.product-image img', {}, 1, 24, 'Foot district')).start()
        Process(target = self.imageLxml, args = ('https://www.uebervart-shop.de/shop/', 'article.one-third a', 'article.one-third a', 'article.one-third img', {}, 1, 24, 'Uebevart shop')).start()
        Process(target = self.imageLxml, args = ('https://slash-store.com/en/14-sneakers', 'a.product-name', 'a.product-name', 'a.product_image img', {}, 1, 24, 'Slash store')).start()
        Process(target = self.imageLxml, args = ('http://www.gloryholeshop.com/http://www.gloryholeshop.com/', 'a.overlay', '', 'div.item img', {}, 1,  24, 'gloryholeshop')).start()
        Process(target = self.imageLxml, args = ('http://www.huntingandcollecting.com/shop/173-footwear', 'a.product_img_link', 'div.product-name', 'a.product_img_link img', {}, 1,  24, 'huntingandcollecting')).start()
        Process(target = self.imageLxml, args = ('https://www.afew-store.com/de/sneaker/', 'a.product-image', 'h2.product-name', 'a.product-image img', {}, 1, 24, 'Afew Store')).start()
        Process(target = self.imageLxml, args = ('http://www.sneakers76.com/en/new-products', 'a.product-name', 'a.product-name', 'img.replace-2x', {}, 1, 24, 'Sneakers 76')).start()
        Process(target = self.imageLxml, args = ('http://www.terracetint.com/shoes', 'h2.product-name a', 'h2.product-name', 'a.product-image img', {}, 1, 24, 'Tint footwear')).start()
        Process(target = self.imageLxml, args = ('https://www.ntrstore.com/sneakers', 'a.product-image', 'h2.product-name', 'a.product-image img', {}, 1, 24, 'unotrestore')).start()
        Process(target = self.imageLxml, args = ('http://www.avenuestore.be/en/collection/', 'a.title', 'a.title', 'div.image-wrap img', {}, 1, 24, 'Avenue Store')).start()
        Process(target = self.imageLxml, args = ('https://glueckstreter.de/shop/', 'div.product-details a', 'div.product-details h3', '', {}, 1, 24, 'glueckstreter')).start()
        Process(target = self.imageLxml, args = ('http://kosmosstore.com/en/13-sneakers-kosmos', 'a.product_img_link', 'div.right-block h5', 'a.product_img_link img', '', 1,  24, 'kosmosstore')).start()
        Process(target = self.imageLxml, args = ('https://www.antonia.it/238-what-s-new', 'a.product_img_link', 'a.product-name', 'a.product_img_link img', '', 1,  24, 'antonia mens')).start()
        Process(target = self.imageLxml, args = ('https://www.antonia.it/237-what-s-new', 'a.product_img_link', 'a.product-name', 'a.product_img_link img', '', 1,  24, 'antonia women')).start()
        Process(target = self.imageLxml, args = ('https://www.excelsiormilano.com/833-what-s-new', 'a.product_img_link', 'a.product-name', 'a.product_img_link img', '', 1,  24, 'excelsiormilano mens')).start()
        Process(target = self.imageLxml, args = ('https://www.excelsiormilano.com/897-shoes', 'a.product_img_link', 'a.product-name', 'a.product_img_link img', '', 1,  24, 'excelsiormilano womens')).start()
        Process(target = self.imageLxml, args = ('http://www.impact-premium.com/fr/nouveaux-produits', 'a.product_img_link', 'a.product-name', 'a.product_img_link img', '', 1,  24, 'impact-premium')).start()
        Process(target = self.imageLxml, args = ('https://www.sotostore.com/latest-products/footwear', 'li.item a', 'div.content', 'img.product-image', '', 1,  24, 'sotostore')).start()
        Process(target = self.imageLxml, args = ('http://www.kasina.co.kr/goods/populate.php', 'div.thumbnail a', 'div.txt', 'div.thumbnail img', {}, 1,  24, 'kasina')).start()
        Process(target = self.imageLxml, args = ('http://www.blacksheeplab.com/nike-zoom-mercurial-xl-flyknit/', 'a.product-category', 'a.product-category h6', 'a.product-category img', {}, 1, 24, 'footish')).start()
        Process(target = self.imageLxml, args = ('http://www.summer-store.com/fr/7-nouveautes', 'a.product_img_link', 'h1.product-title', 'img.replace-2x', {}, 1, 24, 'Summer Store')).start()
        Process(target = self.imageLxml, args = ('http://en.km20.ru/catalog/men/new/', 'a.cat_item', 'span.cat_item_name', 'span.cat_item_img img', {}, 1, 24, 'KM 20')).start()
        Process(target = self.imageLxml, args = ('http://www.thenextdoor.fr/en/41-new', 'a.product-name', 'a.product-name', 'img.replace-2x', {}, 1, 24, 'The Next Door France')).start()
        Process(target = self.imageLxml, args = ('https://www.overkillshop.com/en/sneaker.html', 'a.product-name', 'a.product-name', 'a.product-image img', {}, 1, 24, 'Overkill Shop')).start()
        Process(target = self.imageLxml, args = ('https://www.milk-store.com/en/146-shoes?orderby=reference&orderway=desc&orderway=desc#', 'a.product-name', 'a.product-name', 'img.replace-2x', {}, 1, 24, 'Milk store')).start()
        Process(target = self.imageLxml, args = ('https://www.sneakerium.com/catalogue-special-nouveautes.html', 'div.ficheArticle a', 'span.nom', 'img.photos', {}, 1, 24, 'Sneakerium')).start()
        Process(target = self.imageLxml, args = ('http://www.urbanjunglestore.com/it/latest-products.html#page=1&top=152&', 'a.product-image', 'h2.product-name', 'a.product-image img', '', 1,  24, 'urbanjunglestore')).start()
        Process(target = self.imageLxml, args = ('https://paxanga.com/shop/en/105-new-arrivals', 'div.product_img_link a', 'div.center_box_container h5', 'div.product_img_link img', '', 1,  24, 'paxanga')).start()
        Process(target = self.imageLxml, args = ('https://footdistrict.com/zapatillas/novedades.html', 'a.product-image', 'h2.product-name', 'a.product-image img', {}, 1, 24, 'Footdistrict')).start()
        Process(target = self.imageLxml, args = ('http://www.blueribbonlab.it/producttype/4-sneakers-lo.aspx?orderby=15#product-grid-toolbar', 'div.product-item a', 'div.product-item', 'div.picture img', {}, 1,  24, 'Blue Ribbon')).start()
        Process(target = self.imageLxml, args = ('http://www.blueribbonlab.it/producttype/1-sneakers-mid.aspx?orderby=15#product-grid-toolbar', 'div.product-item a', 'div.product-item', 'div.picture img', {}, 1,  24, 'Blue Ribbon')).start()
        Process(target = self.imageLxml, args = ('https://www.brutalzapas.com/sneakers-online-men', 'div.container-name-brand a', 'div.container-name-brand a', 'img.img-p', {}, 1,  24, 'butal zapas')).start()
        Process(target = self.imageLxml, args = ('https://www.brutalzapas.com/sneakers-online-women', 'div.container-name-brand a', 'div.container-name-brand a', 'img.img-p', {}, 1,  24, 'butal zapas')).start()
        Process(target = self.imageLxml, args = ('https://mate-store.com/shop/', 'figure.animated-overlay a', 'div.product-details font' , 'figure.animated-overlay img', '', 1,  24, 'mate-store')).start()
        Process(target = self.imageLxml, args = ('http://www.mita-sneakers.co.jp/', 'div.photo a', 'div.box h3' , 'div.photo img', '', 1,  24, 'mita-sneakers')).start()
        Process(target = self.imageLxml, args = ('http://www.nine.fr/sneakers', 'div.thumbnail a', 'div.caption h2' , 'div.thumbnail img', '', 1,  24, 'nine')).start()
        Process(target = self.imageLxml, args = ('https://www.nittygrittystore.com/men/footwear', 'a.product-a', 'div.inner' , 'div.border img', '', 1,  24, 'nittygrittystore')).start()
        Process(target = self.imageLxml, args = ('https://sapatostore.com/new-arrivals-2/', 'a.item-thumb', 'div.item-info font' , 'a.item-thumb img', '', 1,  24, 'sapatostore')).start()
        Process(target = self.imageLxml, args = ('https://www.fuel.com.gr/new-arrivals/new-arrivals-sneakers.html', 'a.product-image', 'h3.pro-name', 'a.product-image img', {}, 1, 24, 'fuel')).start()
        Process(target = self.imageLxml, args = ('http://www.quarantagradi.it/categoria-prodotto/novita/', 'div.product-innercotent a', 'h3.title-product', 'div.product-innercotent img', {}, 1, 24, 'quarantagradi')).start()
        Process(target = self.imageLxml, args = ('https://www.stickabush.com/new-arrivals/sneaker.html', 'div.wrapper a', 'p.name', 'img.lazy', {}, 1,  24, 'stickabush')).start()
        Process(target = self.imageLxml, args = ('https://www.cornerstreet.fr/nouveautes.html', 'a.product-image', 'h2.product-name', 'a.product-image img', {}, 1,  24, 'cornerstreet')).start()
        Process(target = self.imageLxml, args = ('https://chmielna20.pl/menu/obuwie/meskie', 'p.products__item-name a', 'p.products__item-name', 'div.col-sm-4 img', {}, 1,  24, 'chmielna20')).start()
        Process(target = self.imageLxml, args = ('http://www.consortium.co.uk/latest', 'h2.product-name a', 'h2.product-name', 'img.product-image', {}, 1,  24, 'consortium')).start()
        Process(target = self.imageLxml, args = ('http://eleven-store.pl/sklep/en/3-footwear', 'a.product_image', 'div.opcje', 'div.produkt img', {}, 1,  24, 'eleven store')).start()
        Process(target = self.imageLxml, args = ('https://rezetstore.dk/en/varer?page=1', 'div.teaser-content a', 'div.title' , 'div.content img', '', 1,  24, 'rezetstore')).start()
        Process(target = self.imageLxml, args = ('http://tres-bien.com/new-arrivals/', 'li a', 'div.grid-info' , 'li img', '', 1,  24, 'tres-bien')).start()
        Process(target = self.imageLxml, args = ('http://www.zerogravitytarifa.com/products', 'a.product-a', 'h3.product-title' , 'a.product-a img', '', 3,  24, 'zerogravitytarifa')).start()
        Process(target = self.imageLxml, args = ('https://www.queens.cz/kat/1/boty/', 'div.col-xs-6 a', 'div.col-xs-6 a' , 'div.col-xs-6 img', '', 1,  24, 'queens')).start()
        Process(target = self.imageLxml, args = ('https://ist.290sqm.com/Just-Arrived', 'div.image a', 'div.caption font' , 'div.image img', istmHeaders, 1,  24, '290sqm')).start()

    def shopify(self):

        Process(target = self.superSelector, args = ('http://undefeated.com', 'http://undefeated.com/footwear', 'div.views-row', 'div.image a', 'href', 'div.views-row', 'div.title', 'div.views-row', 'img', 'data-src', '', 0, {}, 5, 24, 'undefeted' )).start()
        Process(target = self.shopify, args = ('https://shop.bdgastore.com/', False, True, 'option2', 10, 'Bdga store')).start()
        Process(target = self.shopify, args = ('https://kithnyc.com/', False, True, 'title', 10, 'kith')).start()
        Process(target = self.shopify, args = ('http://www.deadstock.ca/', True, True, 'title', 10, 'deadstock')).start()
        Process(target = self.shopify, args = ('https://shop.exclucitylife.com/', True, True, 'option2', 10, 'exclucity')).start()
        Process(target = self.shopify, args = ('http://shopnicekicks.com/',  True, True, 'option1',  10, 'Shop Nice Kicks')).start()
        Process(target = self.shopify, args = ('https://properlbc.com/', True, True, 'title', 1, 'Propper lbc')).start()
        Process(target = self.shopify, args = ('https://www.featuresneakerboutique.com/', True, True, 'option2', 10, 'Feature sneaker')).start()
        Process(target = self.shopify, args = ('https://www.notre-shop.com/', True, True, 'option1', 10, 'notre shop')).start()
        Process(target = self.shopify, args = ('http://us.bape.com/', False, True, 'option3', 10, 'bape')).start()
        Process(target = self.shopify, args = ('http://wishatl.com/', True, True, 'option1', 10, 'wish atl')).start()
        Process(target = self.shopify, args = ('http://www.highsandlows.net.au/', True, True, 'option1', 10, 'highs and lows')).start()
        Process(target = self.shopify, args = ('https://likelihood.us/',  True, True, 'option1', 10, 'blends')).start()
        Process(target = self.shopify, args = ('https://www.blendsus.com/',  False, True, 'option1', 10, 'blends')).start()
        Process(target = self.shopify, args = ('https://www.xhibition.co/',  True, True, 'option1', 10, 'xhibition')).start()
        Process(target = self.shopify, args = ('https://www.minishopmadrid.com/', False, True, 'option1', 10, 'Mini shop')).start()
        Process(target = self.shopify, args = ('http://packershoes.com/', True, True, 'option1', 10, 'packer shoes')).start()
        Process(target = self.shopify, args = ('http://cncpts.com/', True, True, 'option1', 10, 'concepts')).start()
        Process(target = self.shopify, args = ('https://www.unknwn.com/', True, False, 10, 'unknown'))
        Process(target = self.shopify, args = ('https://www.soleheaven.com/', True, True, 'option1', 10, 'soleheaven')).start()
        Process(target = self.shopify, args = ('https://nomadshop.net/', True, True, 'option1', 10, 'Nomad shop')).start()
        Process(target = self.shopify, args = ('http://www.blkmkt.us/', True, True, 'option1', 10, 'black market')).start()
        Process(target = self.shopify, args = ('http://www.addictmiami.com/', True, True, 'option1', 10, 'addict')).start()
        Process(target = self.shopify, args = ('http://rise45.com/', True, True, 'option1', 10, 'rise45')).start()
        Process(target = self.shopify, args = ('https://www.sneakerworldshop.com/', True, True, 'option1', 10, 'sneakerworldshop')).start()
        Process(target = self.shopify, args = ('https://renarts.com/', True, True, 'option1', 10, 'renarts')).start()
        Process(target = self.shopify, args = ('http://shop.extrabutterny.com/', True, True, 'option1', 10, 'extra butter')).start()
        Process(target = self.shopify, args = ('https://burnrubbersneakers.com/', True, True, 'option1', 10, 'burn rubber')).start()
        Process(target = self.shopify, args = ('https://brooklynwaynyc.com/', True, False, 10, 'brooklen way'))
        Process(target = self.shopify, args = ('http://sneakerpolitics.com/', True, False, 10, 'sneaker politics'))
        Process(target = self.shopify, args = ('https://www.leaders1354.com/',  True, True, 'option1', 10, 'leaders')).start()
        Process(target = self.shopify, args = ('https://www.rimenyc.com/',  True, True, 'option1', 10, 'rimenyc')).start()
        Process(target = self.shopify, args = ('http://www.socialstatuspgh.com/',  True, True, 'option1', 10, 'socialstatus')).start()
        Process(target = self.shopify, args = ('https://concrete.nl/',  True, False, 10, 'concrete'))
        Process(target = self.shopify, args = ('https://us.octobersveryown.com/',  True, True, 'option1', 10, 'OVO shop')).start()
        Process(target = self.shopify, args = ('https://www.solestop.com/', True, True, 'option1', 10, 'Sole stop')).start()
        Process(target = self.shopify, args = ('https://rockcitykicks.com/',  True, True, 'option1', 10, 'Rock city kicks')).start()
        Process(target = self.shopify, args = ('https://www.bowsandarrowsberkeley.com/',  True, True, 'option1', 10, 'bows and arrows berkeley')).start()
        Process(target = self.shopify, args = ('https://shop.bbcicecream.com/',  True, True, 'option2', 10, 'BBC')).start()
        Process(target = self.shopify, args = ('https://www.trophyroomstore.com/', False, True, 'option1', 10, 'Trophy room')).start()
        Process(target = self.shopify, args = ('http://shop.havenshop.ca/', True, True, 10,  'Haven shop'))
        Process(target = self.shopify, args = ('https://atmosny.com/',  True, True, 'option1', 10, 'Atmos NY')).start()
        Process(target = self.shopify, args = ('https://www.oipolloi.com/',  True, True, 'option1', 10, 'Oi Polloi')).start()
        Process(target = self.shopify, args = ('https://offthehook.ca/', True, True, 'option2', 10, 'off the hook')).start()
        Process(target = self.shopify, args = ('https://noirfonce.eu/',  True, True, 'option1', 10, 'noirfonce')).start()
        Process(target = self.shopify, args = ('https://www.thefactoryokc.com/',  True, True, 'option2', 10, 'The factory okc')).start()
        Process(target = self.shopify, args = ('https://www.saintalfred.com/', True,  False, False, 10, 'Saint Alfred')).start()
        Process(target = self.shopify, args = ('https://www.solefly.com/',  True, True, 'option2', 10, 'Solefly')).start()
        Process(target = self.shopify, args = ('https://www.a-ma-maniere.com/', True, True, 'option1', 10, 'A Ma Maniere')).start()
        Process(target = self.shopify, args = ('https://commonwealth-ftgg.com/', True, True , 'option1', 10, 'Common wealth')).start()
        Process(target = self.shopify, args = ('https://www.bbbranded.com/', True, True , 'option2', 10, 'BBbranded')).start()
        Process(target = self.shopify, args = ('https://shophny.com/', True, False, 'option1', 10, 'Shoph NY')).start()
        Process(target = self.shopify, args = ('https://beatniconline.com/', True, True, 'option1', 10, 'Beatniconline')).start()
        Process(target = self.shopify, args = ('https://www.dipstreet.co.za/', True, True, 'option1', 10, 'dipstreet')).start()
        Process(target = self.shopify, args = ('https://www.goodasgold.co.nz/', True, True, 'option1', 10, 'goodasgold')).start()
        Process(target = self.shopify, args = ('https://www.dope-factory.com/', True, True, 'option1', 10, 'dope-factory')).start()
        Process(target = self.shopify, args = ('https://hoohastore.com/', True, True, 'option1', 10, 'dope-factory')).start()
        Process(target = self.shopify, args = ('https://store.hombreamsterdam.com/', True, True, 'option1', 10, 'hombreamsterdam')).start()
        Process(target = self.shopify, args = ('https://shop-usa.palaceskateboards.com', True, False, 'option1', 10, 'palaceskateboards')).start()
        Process(target = self.shopify, args = ('https://www.incu.com/', True, True, 'option1', 10, 'incu')).start()
        Process(target = self.shopify, args = ('https://www.kongonline.co.uk/', True, True, 'option1', 10, 'kongonline')).start()
        Process(target = self.shopify, args = ('https://www.philipbrownemenswear.co.uk/', True, True, 'option1', 10, 'philipbrownemenswear')).start()
        Process(target = self.shopify, args = ('https://www.rooneyshop.com/', True, True, 'option1', 10, 'rooneyshop')).start()
        Process(target = self.shopify, args = ('https://suede-store.com/', True, True, 'option1', 10, 'Suede Store')).start()
        Process(target = self.shopify, args = ('https://astoreisgood.com/', True, True, 'option1', 10, 'A Store is good')).start()
        Process(target = self.shopify, args = ('https://nrml.ca/', True, True, 'Title', 10, 'Nrml')).start()
        Process(target = self.shopify, args = ('https://18montrose.com/', True, True, 'option1', 10, '18montrose')).start()
        Process(target = self.shopify, args = ('https://www.alumniofny.com/', True, True, 'option1', 10, 'alumniofny')).start()

    def maybe(self):
        #Yes
        Process(target = self.imageLxml, args = ('http://www.billys-tokyo.net/shop/r/r1010_j1/', 'a.image', 'div.name', 'a.image img', {}, 1, 24, 'billys-tokyo')).start()
        Process(target = self.imageLxml, args = ('https://www.le-fix.com/footwear/', 'a.product-image', 'h2.product-name', 'a.product-image img', {}, 1,  24, 'le-fix')).start()
        Process(target = self.imageLxml, args = ('https://gr8.jp/eshop/gr8/', 'div.bubble a', 'h3.list-title', 'div.bubble img', {}, 1,  24, 'gr8')).start()
        Process(target = self.lxmlNeverTweetSameThing, args = ('https://www.farfetch.com', 'https://www.farfetch.com/shopping/men/shoes-2/items.aspx?ffref=hd_snav&sort=2', 'article.baseline', 'a', 'href', 'article.baseline', 'a.listing-item-content', 'article.baseline', 'img.imageRollover', 'src', '', 0, {}, 1, 'farfetch')).start()
        Process(target = self.imageLxml, args = ('https://www.main-source.co.uk/footwear.html', 'a.product-image', 'div.brand-name', 'a.product-image img', '', 1,  24, 'main-source')).start()
        Process(target = self.imageLxml, args = ('http://lerayonfrais.fr/en/102-sneakers?', 'div.thumb_picture a', 'div.thumb_title' , 'div.thumb_picture img', '', 1,  24, 'lerayonfrais')).start()
        Process(target = self.imageLxml, args = ('http://www.urbanshooz.fr/fr/nouveaux-produits', 'a.uk-display-block', 'a.uk-text-truncate span', 'a.uk-display-block img', {}, 1, 24, 'urbanshooz')).start()
        Process(target = self.imageLxml, args = ('http://dangerousminds.gr/greek/men/footwear-mens/latest.html', 'a.product-image', 'div.product-info h2', 'a.product-image img', {}, 1, 24, 'dangerousminds')).start()
        Process(target = self.imageLxml, args = ('http://www.michaelknyc.com/footwear/?search_query=&page=1&limit=100&sort=newest&category=1020&is_category_page=1', 'div.ProductImage a', 'a.pname' , 'div.ProductImage img', '', 1,  24, 'michaelknyc')).start()
        Process(target = self.imageLxml, args = ('http://deliberti.it/ultimi_arrivi.php?uomodonna=2&page=1#to', 'p.s001_c a', 'p.s001_c', 'a.thumbnail img', {}, 1,  24, 'deliberti')).start()

        #No
        Process(target = self.superSelector, args = ('http://www.drome.co.uk', 'http://www.drome.co.uk/new-mens-footwear/', 'div.prodlistwrap', 'a.fc-lightmidgrey', 'href', 'div.prodlistwrap', 'div.prodinfos', 'div.prodlistwrap', 'img', 'src', 'http://www.drome.co.uk', 0, {}, 1, 24, 'drome')).start()
        Process(target = self.superSelector, args = ('http://www.soulfoot.de', 'http://www.soulfoot.de/de/Sneaker/Sneaker,10,1.html', 'article.categoryOverviewArticleContainer', 'a.articleDetails', 'href', 'article.categoryOverviewArticleContainer', 'h2.articleName', 'article.categoryOverviewArticleContainer', 'div.articleImageContainer img', 'data-src', 'http://www.soulfoot.de', 0, {}, 1, 24, 'soulfoot' )).start()
        Process(target = self.superSelector, args = ('http://www.comingsoonshop.com', 'http://www.comingsoonshop.com/fr/catalog/c13~sneakers?pageindex=1', 'div.catalog-product-list__product-list__item', 'a', 'href', 'div.catalog-product-list__product-list__item', 'h3.product-title', 'div.catalog-product-list__product-list__item', 'img', 'src', 'http://www.comingsoonshop.com', 0, {}, 1, 24, 'comingsoonshop')).start()
        Process(target = self.imageLxml, args = ('https://www.graffitishop.net/Sneakers-Streetwear', 'div.listbox a', 'h3.pname', 'div.thumb img',  {}, 1,  24, 'graffitishop')).start()
        Process(target = self.imageLxml, args = ('https://www.hanon-shop.com/c/q/department/footwear', 'div.product a', 'span.prod-name', 'div.product img', {}, 1, 24, 'hanon-shop')).start()
        Process(target = self.imageLxml, args = ('https://www.hypedc.com/footwear?dir=desc&order=news_from_date', 'div.item a', 'div.col-xs-24', 'div.unveil-container img', {}, 1,  24, 'hypedc')).start()
        Process(target = self.imageLxml, args = ('http://piils.fr/sneakers-10', 'a.product_img_link', 'a.product-name', 'a.product_img_link img', {}, 1, 24, 'piils')).start()
        Process(target = self.imageLxml, args = ('http://www.animal-tracks.de/products_new.php', 'div.contentList a', 'div.contentList', 'div.contentList img', {}, 1,  24, 'animal-tracks')).start()
        Process(target = self.imageLxml, args = ('http://www.blackrainbow-shop.com/en/new-products', 'p a', 'span.name', 'li.first img', {}, 1, 24, 'BlackRainbow Shop')).start()
        Process(target = self.imageLxml, args = ('https://www.le-fix.com/footwear', 'a.product-image', 'h2.product-name', 'a.product-image img', '', 1,  24, 'le-fix')).start()
        Process(target = self.imageLxml, args = ('http://www.saintcream.com/', 'a.product_image', 'h5.product_name' , 'a.product_image img', '', 1,  24, 'saintcream')).start()
        Process(target = self.imageLxml, args = ('https://www.schrittmacher-shop.de/', 'div.kat a', 'a.ArtikelLink' , 'div.kat img', '', 1,  24, 'schrittmacher-shop')).start()
        Process(target = self.imageLxml, args = ('http://shelta.eu/products/category/sneakers-footwear/overview', 'div.product-thumb a', 'div.product-desc h4', 'div.product-thumb img', {}, 1, 24, 'shelta')).start()
        Process(target = self.imageLxml, args = ('https://www.citadium.com/fr/fr/sneakers-homme', 'a.img', 'div.pLib', 'a.img img', {}, 1,  24, 'citadium')).start()
        Process(target = self.imageLxml, args = ('http://www.dr-adams.dk/nyevare-men', 'ul.list-commodity a', 'span.list-commodity-title', 'span.list-commodity-image img', {}, 1,  24, 'dr-adams')).start()


    def needsWork(self):
        #Yes
        Process(target = self.imageLxml, args = ('http://www.footure.hu/cikkek/ujdonsagok/pag_ujdonsagok.aspx', 'div.col-lg-5ths a', 'div.product-content h2', 'div.product-image img', {}, 1,  24, 'footure')).start()
        Process(target = self.imageLxml, args = ('http://www.rapcity.hu/cikkek/ujdonsagok/pag_ujdonsagok.aspx', 'a.cl-item', 'div.cl-item-overlay img' , 'h2.cl-item-title', {}, 1,  24, 'rapcity')).start()

        #No
        Process(target = self.imageLxml, args = ('http://www.loadednz.com/products/footwear', 'div.image a', 'div.style', 'div.image img', loadedHeaders, 3, 24, 'Loadednz')).start()

        Process(target = self.imageLxml, args = ('http://www.streetconnexion.fr/187-nouveautes?id_category=187&n=33#/', 'a.product_img_link', 'a.product-name', 'a.product_img_link img', '', 1,  24, 'streetconnexion')).start()
        Process(target = self.imageLxml, args = ('http://www.susi.it/prodotti-sector/uomo?categorySlug=Scarpe%20Sneaker&activitySlug=full', 'div.isotope a', 'div.title', 'div.isotope img', {}, 1, 24, 'Susi men sneaker')).start()
        Process(target = self.imageLxml, args = ('http://www.susi.it/prodotti-sector/uomo?categorySlug=LTD%20EDITION&activitySlug=full', 'div.isotope a', 'div.title', 'div.isotope img', {}, 1, 24, 'Susi men ltd')).start()
        Process(target = self.imageLxml, args = ('http://www.susi.it/prodotti-sector/donna?categorySlug=Scarpe%20Sneaker&activitySlug=full', 'div.isotope a', 'div.title', 'div.isotope img', {}, 1, 24, 'Susi women sneaker')).start()
        Process(target = self.imageLxml, args = ('https://www.1st-og.ch/sneakers', 'a.product-name', 'span.name', 'a.product-image img', {}, 1, 24, '1st OG')).start()
        Process(target = self.imageLxml, args = ('https://en.titolo.ch/brands', 'div.img-wrapper a', 'span.name', 'a.product-image img', {}, 1, 24, 'Titolo')).start()
        Process(target = self.imageLxml, args = ('https://www.patta.nl/new-arrivals/footwear', 'h3.product-name a', 'h3.product-name', 'span.hover-image img', pataHeaders, 1, 24, 'Patta')).start()
        Process(target = self.superSelector, args = ('', 'https://www.saveoursole.de/sneaker/?p=2', 'div.product--box', 'a.product--image', 'href', 'div.product--box', 'a.product--title', 'div.product--box', 'span.image--media img', 'srcset', '', 0, {}, 1, 24, 'Save our soul' )).start()
        Process(target = self.imageLxml, args = ('https://www.nighshop.com/', 'div.content a', 'div.name', 'div.image img', nighHeaders, 1, 12, 'NIGH shop')).start()
        Process(target = self.basicSitemap, args = ('http://shop.doverstreetmarket.com/sitemap.xml', DSMheaders, 2, 24, 'doverstreetmarket')).start()
        Process(target = self.imageLxml, args = ('https://www.sneakersnstuff.com/en/2/sneakers', 'li.product a', 'div.info', 'img.campaign', snsHeaders, 5, 24, 'sneakersnstuff')).start()
        Process(target = self.imageLxml, args = ('http://stormfashion.dk/new', 'div.pro_txt a', 'div.pro_txt h3', 'div.pro_img img', {}, 1, 24, 'stormfashion')).start()
        Process(target = self.imageLxml, args = ('https://www.ssense.com/en-us/men/designers/adidas-originals/shoes', 'div.browsing-product-item a', 'p.hidden-smartphone-landscape', 'img.product-thumbnail', {}, 1, 0, 'SSense')).start()
        Process(target = self.imageLxml, args = ('https://www.ssense.com/en-us/men/designers/yeezy/shoes', 'div.browsing-product-item a', 'p.hidden-smartphone-landscape', 'img.product-thumbnail', {}, 1, 0, 'SSense')).start()
        Process(target = self.imageLxml, args = ('http://shibuya-quality-store.fr/fresh-news/pages/1-2/', 'li.product a', 'span.productTitle', 'img.attachment-shop_catalog', {}, 1, 24, 'Shibuya quality store')).start()
        Process(target = self.imageLxml, args = ('https://caliroots.com/news/s/20?p=128406&p=94509&p=222765&p=94784&p=124010&p=100518&p=103368&p=98890&p=97907&p=94876&p=91492&orderBy=Published', 'li.product a', 'p.name', 'div.image img', {}, 1, 24, 'Caliroots')).start()
        Process(target = self.imageLxml, args = ('http://www.impactshop.fr/en/33-new-products', 'h3.name a', 'h3.name a', 'img.replace-2x', {}, 1, 24, 'Impact shop')).start()
        Process(target = self.imageLxml, args = ('https://www.afew-store.com/de/adidas/yeezy/', 'a.product-image', 'h2.product-name', 'a.product-image img', {}, 1, 24, 'Afew Store Yeezy Page')).start()
        Process(target = self.imageLxml, args = ('https://www.vrients.com/usa/footwear.html', 'a.product-image', 'div.product-info', 'img.first', '', 1,  24, 'vrients')).start()
        Process(target = self.imageLxml, args = ('https://www.impactshoes.com/en/les-nouveautes', 'div.field-content a', 'div.views-field', 'img.img-responsive', '', 1,  24, 'impactshoes')).start()
        Process(target = self.imageLxml, args = ('https://www.inner.eu/en/US/section/categories/footwear', 'article.product a', 'div.brand-name', 'img.top', '', 1,  24, 'inner')).start()
        Process(target = self.imageLxml, args = ('http://www.phenomglobal.com/product-category/footwear/', 'figure.product-transition a', 'div.product-details h3' , 'div.product-image img', '', 1,  24, 'phenomglobal')).start()

cook().test()

