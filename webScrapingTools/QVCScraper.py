import requests, json, csv
from bs4 import BeautifulSoup
from datetime import datetime

fnDateStamp = datetime.now().strftime('%m-%d-%Y')
header = ['BARCODE','COLOR','DESCRIPTION', 'PRICE', 'URL']
inputFile = 'barcodes.txt'
productArray = []

def barcodes(): #Open new line delimited text file of scanned item.
	skuArray = []
	with open(inputFile, 'r') as skus:
		for sku in skus.readlines():
			#print sku,
			skuArray.append(sku.replace('\n', ''))
	return skuArray

def getURLOf(sku): # parse passed sku to construct/determine URL
	prefix = 'http://www.qvc.com/product.'
	suffix = '.html'

	root = sku[0:7]
	url = '%s%s%s' % (prefix, root, suffix)
	return url

def getDetailsFrom(sku, url): # Output array of details scraped from products url. Formatting conforms to header above.
	colorOptions = []

	get = requests.get(url)
	htmlSource = get.content
	soup = BeautifulSoup(htmlSource, 'html.parser')

	itemTitle = soup.find_all('h1')[0].get_text()
	#itemNumber = soup.find_all(class_='itemNo')[0].get_text()

	buyBox = soup.find_all('div', class_='buyBoxPricing')
	compPrice = buyBox[0].find_all('p', class_='rvPrice')
	price = compPrice[0].find_all('span')[0].get_text().replace('\t', '').replace('\n', '').replace('  ', '')

	#price = compPrice[0].attrs['rvPrice']
	#clearancePrice = buyBox[0].find_all('span', class_='productDetailPrice')[0]
	#price = clearancePrice.get_text().replace('\t', '').replace('\n', '')

	colorVariations = soup.find_all('ul', class_='buyBoxColorList')
	colorList = colorVariations[0].find_all('li')#.attrs#find_all('title').attrs

	colorOptions = []
	for colors in colorList:
		color = colors.attrs['title']
		colorOptions.append('%s' % color)

	#IF GETTING ALL COLOR VARIATIONS#
	#listing = '%s, %s, %s, [%s]\n' % (itemNumber, itemTitle, price, ','.join(str(x) for x in colorOptions))

	#listing = '%s, [%s], %s, %s, %s\n' % (sku, ','.join(str(x) for x in colorOptions), itemTitle, price, url)
	listing = [sku, [','.join(str(x) for x in colorOptions)], itemTitle, price, url]
	productArray.append(listing)
	#print productDetails
	return listing

def ifSoldOut(barcode, url): # If item is sold out, pricing/description is invisible. Perform different scraping methods.
	get = requests.get(url)
	htmlSource = get.content
	soup = BeautifulSoup(htmlSource, 'html.parser')

	itemTitle = soup.find_all('h1')[0].text.lstrip(' ')

	retailPriceIfSoldOut = soup.find_all(id='productJSON')
	productJson = json.loads(retailPriceIfSoldOut[0].text)['atsByColor']
	firstProduct = productJson.keys()[0]
	price = productJson[firstProduct]['qvcPrice']

	listing = [barcode, '', itemTitle, price, url]
	productArray.append(listing)
	#print productDetails
	return listing

with open('lookupTable-%s.csv' % fnDateStamp, 'w') as output: # master log file, output lookup table
	writer = csv.writer(output, delimiter=',', lineterminator='\n')
	writer.writerow(header)

	for barcode in barcodes():
		url = getURLOf(barcode)
		try:
			listing = getDetailsFrom(barcode, url)

		except:
			try:
				listing = ifSoldOut(barcode, url)
			except:
				listing == barcode
		finally:
			print listing
			writer.writerow(listing)

output.close()