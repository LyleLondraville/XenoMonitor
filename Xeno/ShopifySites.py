# TODO : Upload code to servers
# TODO : Test Shopify funct
# TODO : Run other functions and featuers


from multiprocessing import Process
from Shopify import shopy
import requests 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Process(target = self.shopify, args = ('https://www.dipstreet.co.za/', True, 'option1', 3, 'dipstreet')).start()
# Process(target = self.shopify, args = ('https://www.goodasgold.co.nz/', True, 'option1', 3, 'goodasgold')).start()
# Process(target = self.shopify, args = ('https://www.dope-factory.com/', True, 'option1', 3, 'dope-factory')).start()
# Process(target = self.shopify, args = ('http://us.bape.com/', False, 'option3', 3, 'bape')).start()
# Process(target = self.shopify, args = ('https://hoohastore.com/', True, 'option1', 3, 'dope-factory')).start()
# Process(target = self.shopify, args = ('https://shop-usa.palaceskateboards.com', True, 'option1', 3, 'palaceskateboards')).start()
# Process(target = self.shopify, args = ('https://www.sneakerworldshop.com/', True, 'option1',3, 'sneakerworldshop')).start()
# Process(target = self.shopify, args = ('https://burnrubbersneakers.com/', True, 'option1', 3, 'burn rubber')).start()
# Process(target = self.shopify, args = ('https://www.leaders1354.com/',  True, 'option1',3, 'leaders')).start()
# Process(target = self.shopify, args = ('https://concrete.nl/',  True, 3, 'concrete'))
# Process(target = self.shopify, args = ('https://www.incu.com/', True, 'option1',3, 'incu')).start()
# Process(target = self.shopify, args = ('https://www.philipbrownemenswear.co.uk/', True, 'option1',3, 'philipbrownemenswear')).start()
# Process(target = self.shopify, args = ('https://www.solestop.com/', True, 'option1', 3, 'Sole stop')).start()
# Process(target = self.shopify, args = ('https://shop.bbcicecream.com/',  True, 'option2', 3, 'BBC')).start()
# Process(target = self.shopify, args = ('http://shop.havenshop.ca/', True, 3,  'Haven shop'))
# Process(target = self.shopify, args = ('https://atmosny.com/',  True, 'option1', 3, 'Atmos NY')).start()
# Process(target = self.shopify, args = ('https://www.oipolloi.com/',  True, 'option1', 3, 'Oi Polloi')).start()
# Process(target = self.shopify, args = ('https://www.bbbranded.com/', True, True , 'option2', 3, 'BBbranded')).start()
# Process(target = self.shopify, args = ('https://shophny.com/', True, False, 'option1', 3, 'Shoph NY')).start()
# Process(target = self.shopify, args = ('https://beatniconline.com/', True, True, 'option1', 3, 'Beatniconline')).start()
# Process(target = self.shopify, args = ('https://www.rooneyshop.com/', True, True, 'option1', 3, 'rooneyshop')).start()
# Process(target = self.shopify, args = ('https://www.saintalfred.com/', True,  False, False, 3, 'Saint Alfred')).start()
# Process(target = self.shopify, args = ('https://astoreisgood.com/', True, True, 'option1', 3, 'A Store is good')).start()
# Process(target = self.shopify, args = ('https://18montrose.com/', True, True, 'option1', 3, '18montrose')).start()


class shopifyMethods(shopy):

	def __init__(self):

		self.genIps =['45.76.251.33',
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

		self.deadStock = ['45.33.56.7', '45.33.48.203']
		self.snk = ['96.126.97.207', '45.33.40.42']
		self.wish = ['45.33.108.205', '192.155.85.17']
		self.high = ['45.56.88.165', '45.56.80.202']
		self.packer = ['104.237.152.178', '23.239.5.119']
		self.cncp = ['23.92.25.240', '66.175.221.199']
		self.blkmkt = ['173.255.218.200	', '198.74.49.54']
		self.addic = ['173.255.210.152', '173.230.153.5']



	def goodSites(self):
		Process(target = self.shopify, args = ('https://shop.bdgastore.com/', False, self.genIps, 'option2', 0, 'Bdga store')).start()
		Process(target = self.shopify, args = ('https://kithnyc.com/', False, self.genIps, 'title', 0, 'kith')).start()
		Process(target = self.shopify, args = ('https://shop.exclucitylife.com/', True, self.genIps, 'option2', 0, 'exclucity')).start()
		Process(target = self.shopify, args = ('https://likelihood.us/',  True, self.genIps, 'option1', 0, 'blends')).start()
		Process(target = self.shopify, args = ('https://www.blendsus.com/',  False, self.genIps, 'option1', 0, 'blends')).start()
		Process(target = self.shopify, args = ('https://www.xhibition.co/',  True, self.genIps, 'option1', 0, 'xhibition')).start()
		Process(target = self.shopify, args = ('https://www.minishopmadrid.com/', False, self.genIps, 'option1', 0, 'Mini shop')).start()
		Process(target = self.shopify, args = ('https://www.unknwn.com/', True, 0, self.genIps, 'unknown'))
		Process(target = self.shopify, args = ('https://www.soleheaven.com/', True, self.genIps, 'option1', 0, 'soleheaven')).start()
		Process(target = self.shopify, args = ('https://nomadshop.net/', True, self.genIps, 'option1', 0, 'Nomad shop')).start()
		Process(target = self.shopify, args = ('https://store.hombreamsterdam.com/', True, self.genIps, 'option1', 0, 'hombreamsterdam')).start()
		Process(target = self.shopify, args = ('https://brooklynwaynyc.com/', True, self.genIps, "", 0, 'brooklen way'))
		Process(target = self.shopify, args = ('http://sneakerpolitics.com/', True, self.genIps, "", 0, 'sneaker politics'))
		Process(target = self.shopify, args = ('https://www.rimenyc.com/',  True, self.genIps, 'option1',0, 'rimenyc')).start()
		Process(target = self.shopify, args = ('https://renarts.com/', True, self.genIps, 'option1',0, 'renarts')).start()
		Process(target = self.shopify, args = ('https://www.kongonline.co.uk/', True, self.genIps, 'option1',0, 'kongonline')).start()
		Process(target = self.shopify, args = ('https://us.octobersveryown.com/',  True, self.genIps, 'option1', 0, 'OVO shop')).start()
		Process(target = self.shopify, args = ('https://rockcitykicks.com/',  True, self.genIps, 'option1', 0, 'Rock city kicks')).start()
		Process(target = self.shopify, args = ('https://www.bowsandarrowsberkeley.com/',  True, self.genIps, 'option1', 0, 'bows and arrows berkeley')).start()
		#Process(target = self.shopify, args = ('https://www.trophyroomstore.com/', False, self.genIps, 'option1', 0, 'Trophy room')).start()
		#Process(target = self.shopify, args = ('https://offthehook.ca/', True, self.genIps, 'option2', 0, 'off the hook')).start()
		#Process(target = self.shopify, args = ('https://noirfonce.eu/',  True, self.genIps, 'option1', 0, 'noirfonce')).start()
		#Process(target = self.shopify, args = ('https://www.solefly.com/',  True, self.genIps, 'option2', 0, 'Solefly')).start()
		#Process(target = self.shopify, args = ('https://www.a-ma-maniere.com/', True, self.genIps, 'option1', 0, 'A Ma Maniere')).start()
		#Process(target = self.shopify, args = ('https://commonwealth-ftgg.com/', True, self.genIps, 'option1', 0, 'Common wealth')).start()
		#Process(target = self.shopify, args = ('https://suede-store.com/', True,  self.genIps, 'option1', 0, 'Suede Store')).start()
		#Process(target = self.shopify, args = ('https://nrml.ca/', True, self.genIps, 'Title', 0, 'Nrml')).start()
		#Process(target = self.shopify, args = ('https://www.alumniofny.com/', True,  self.genIps, 'option1', 0, 'alumniofny')).start()

	def bitchSites(self):

		Process(target = self.shopify, args = ('http://www.deadstock.ca/', True, self.deadStock, 'title', 3, 'deadstock')).start()
		Process(target = self.shopify, args = ('http://shopnicekicks.com/',  True, self.snk, 'option1',  3, 'Shop Nice Kicks')).start()
		Process(target = self.shopify, args = ('http://wishatl.com/', True, self.wish, 'option1', 3, 'wish atl')).start()
		Process(target = self.shopify, args = ('http://www.highsandlows.net.au/', True, self.high, 'option1', 3, 'highs and lows')).start()
		Process(target = self.shopify, args = ('http://packershoes.com/', True, self.packer, 'option1', 3, 'packer shoes')).start()
		Process(target = self.shopify, args = ('http://cncpts.com/', True, self.cncp, 'option1', 3, 'concepts')).start()
		#Process(target = self.shopify, args = ('http://www.blkmkt.us/', True, self.blkmkt, 'option1', 1, 'black market')).start()
		Process(target = self.shopify, args = ('http://www.addictmiami.com/', True, self.addic, 'option1', 3, 'addict')).start()
		#Process(target = self.shopify, args = ('http://rise45.com/', True,  self.blkmkt, 'option1',1, 'rise45')).start()
		#Process(target = self.shopify, args = ('http://shop.extrabutterny.com/', True, 'option1',1, 'extra butter')).start()
		#Process(target = self.shopify, args = ('http://www.socialstatuspgh.com/',  True, 'option1',1, 'socialstatus')).start()




s = shopifyMethods()
s.bitchSites()
