import requests, mechanize
from bs4 import BeautifulSoup
from datetime import datetime

br = mechanize.Browser()

inputFile = 'barcodes.txt'
urlFile = 'urls.txt'
outputFile = 'lookupTable-%s.txt' % datetime.now().strftime('%m-%d-%Y')
productDetails = []

def getURL(sku):
	staticUrl = "http://www.qvc.com"
	productID = sku[0:7]

	response = br.open(staticUrl)
	br.select_form(nr = 0)
	br.form['keyword'] = productID
	response2 = br.submit()
	url = response2.geturl()

	with open(urlFile, 'a+') as urls:
		urls.write('%s, %s\n' % (sku.replace('\n', ''), url))
	return url

def productDetailsFrom(url):
	colorOptions = []

	with open(urlFile, 'r') as urls:
		for url in urls.readlines():
			sku = url.split(',')[0]
			url = url.split(',')[1]

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

	listing = '%s, %s, %s, [%s]\n' % (sku, itemTitle, price, ','.join(str(x) for x in colorOptions))
	productDetails.append(listing)
	print productDetails
	return listing

with open(inputFile, 'r') as f:
	for sku in f.readlines():
		with open(outputFile, 'a+') as out:
			out.write('%s' % productDetailsFrom(getURL(sku)))