from threading import Thread
from multiprocessing import Process

from Scrapers import Scrape
import requests

try :
    urllib3
    urllib3.disable_warnings()
except :
    pass

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class cook(Scrape):

    def start(self):

        Process(target=self.meshCommerceScrape, args=("footpatrol", 0, 100000)).start()
        Process(target=self.meshCommerceScrape, args=("footpatrol", 100000, 200000)).start()
        Process(target=self.meshCommerceScrape, args=("footpatrol", 200000, 300000)).start()
        Process(target=self.meshCommerceScrape, args=("footpatrol", 300000, 400000)).start()
        Process(target=self.meshCommerceScrape, args=("footpatrol", 400000, 500000)).start()
        Process(target=self.meshCommerceScrape, args=("footpatrol", 500000, 600000)).start()
        Process(target=self.meshCommerceScrape, args=("footpatrol", 600000, 700000)).start()
        Process(target=self.meshCommerceScrape, args=("footpatrol", 700000, 800000)).start()
        Process(target=self.meshCommerceScrape, args=("footpatrol", 800000, 900000)).start()
        Process(target=self.meshCommerceScrape, args=("footpatrol", 900000, 999999)).start()

        Process(target=self.meshCommerceScrape, args=("size", 0, 100000)).start()
        Process(target=self.meshCommerceScrape, args=("size", 100000, 200000)).start()
        Process(target=self.meshCommerceScrape, args=("size", 200000, 300000)).start()
        Process(target=self.meshCommerceScrape, args=("size", 300000, 400000)).start()
        Process(target=self.meshCommerceScrape, args=("size", 400000, 500000)).start()
        Process(target=self.meshCommerceScrape, args=("size", 500000, 600000)).start()
        Process(target=self.meshCommerceScrape, args=("size", 600000, 700000)).start()
        Process(target=self.meshCommerceScrape, args=("size", 700000, 800000)).start()
        Process(target=self.meshCommerceScrape, args=("size", 800000, 900000)).start()
        Process(target=self.meshCommerceScrape, args=("size", 900000, 999999)).start()

        Process(target=self.barneyImageScrape, args=(503000000, 503500000)).start()
        Process(target=self.barneyImageScrape, args=(503500000, 504000000)).start()
        Process(target=self.barneyImageScrape, args=(504000000, 504500000)).start()
        Process(target=self.barneyImageScrape, args=(504500000, 505000000)).start()
        Process(target=self.barneyImageScrape, args=(505000000, 505500000)).start()
        Process(target=self.barneyImageScrape, args=(505500000, 505999999)).start()


cook().start()
