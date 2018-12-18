from threading import Thread
from multiprocessing import Process
from time import sleep

from Restocks import Restock
import requests

try :
    import urllib3
    urllib3.disable_warnings()
except :
    pass

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class cook(Restock):

    def server1(self):

        hdrs = {
            'Host': 'solewingedsneaks.bigcartel.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8'
        }

        Process(target = self.pageContentChange, args = ('https://footdistrict.com/zapatillas/novedades.html', '', {}, 1, 'FootDistrict')).start()
        Process(target = self.textRestock, args = ('https://footdistrict.com/zapatillas/novedades.html', '', 'h2.product-name' {}, 1, 'FootDistrict')).start()
        Process(target = self.codeChange, args = ("RUN SCRAPE"))
        #Thread(target = self.barneyPIDrestock, args=('504803872', )).start()
        #Thread(target = self.meshCommerceRestock, args = ('size', '280348')).start()
        #Process(target = self.shopRestock, args=('https://shopnicekicks.com/collections/new-arrivals-1/products/adidas-new-york-arsham-mens-shoe-white', 2)).start()
        #Process(target = self.pageContentChange, args = ('http://solewingedsneaks.bigcartel.com/', 'https://i1.adis.ws/t/jpl/sz_product_list?plu=sz_284362_a&qlt=80&w=300&h=337&v=1', hdrs, 3, 'Test Page Content')).start()
        #sleep(1)
        #Thread(target = self.textRestock, args = ('http://solewingedsneaks.bigcartel.com/', 'https://i1.adis.ws/t/jpl/sz_product_list?plu=sz_284362_a&qlt=80&w=300&h=337&v=1', '', hdrs, 3, 'Test Text Content')).start()
        #sleep(1)
        #Thread(target = self.codeChange, args = ('http://solewingedsneaks.bigcartel.com/product/test', 'https://i1.adis.ws/t/jpl/sz_product_list?plu=sz_284362_a&qlt=80&w=300&h=337&v=1', hdrs, 3, 'Test Status Code')).start()


c = cook()
c.server1()
