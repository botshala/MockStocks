import requests
from bs4 import BeautifulSoup as bs
def get_code(name):
	get_code = 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup?input=%s'%(name)
	soup=bs(requests.get(get_code).text)
	# print soup
	data = soup.find_all('symbol')
	# print data
	code = data[0].text
	print 'code=%s'%code
	return code