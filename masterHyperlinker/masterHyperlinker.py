import os, sys, mechanize
import unicodecsv, xlrd, csv

br = mechanize.Browser()

fileName = 'Evine Domestics load 1-4-18'
inputXLS = '%s.xlsx' % fileName
convertedCSV = 'Converted-%s.csv' % fileName
hyperlinkFile = 'Hyperlinked-%s.csv' % fileName

def xls2csv(xlsFile, csvFile): # Kudos to https://www.penwatch.net/cms/excel_to_csv/
    workbook = xlrd.open_workbook(xlsFile)
    sheet = workbook.sheet_by_index(0)
    file = open(csvFile, "wb")
    csvOutput = unicodecsv.writer(file, encoding='utf-8')

    for row in xrange(sheet.nrows):
        csvOutput.writerow(sheet.row_values(row))
    file.close()

def master(row, skuIndex, titleIndex, url):
	sku = row[skuIndex]
	if len(sku) > 2:
		url = ('%s%s' % (url, sku))
		title = row[titleIndex].rstrip().lstrip().replace('"', '').replace(')', '')
		hyperlinkText = '=HYPERLINK("%s","%s")\n' % (url, title)
		
		row[titleIndex] = hyperlinkText
		#print row
		writer.writerow(row)
	else:
		writer.writerow('\n')

xls2csv(inputXLS, convertedCSV)
with open(convertedCSV, 'r') as vert:
	reader = csv.reader(vert)
	with open(hyperlinkFile, 'wb+') as hyper:
		writer = csv.writer(hyper)
		for line in reader:
			if sys.argv[1] == 'fingerhut':
				print 'Need Example For Indexes'#fingerHut(line, writer)
			elif sys.argv[1] == 'sportsman':
				print 'Need Example For Indexes'#sportsMan(line, writer)
			elif sys.argv[1] == 'evine':
				master(line, 1, 4, 'http://www.evine.com/Product/')
			elif sys.argv[1] == 'amazon':
				print 'Need Example For Indexes'#amazon(line, writer)
			elif sys.argv[1] == 'stoneberry':
				print 'Need Example For Indexes'#stoneBerry(line, writer)
			else:
				print 'poo poo'
		print 'Converted and Linked!'
	hyper.close()
vert.close()
