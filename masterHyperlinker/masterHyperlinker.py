import os, sys, mechanize
import unicodecsv, xlrd, csv

br = mechanize.Browser()

def xls2csv(xlsFile, csvFile): # Kudos to https://www.penwatch.net/cms/excel_to_csv/
    workbook = xlrd.open_workbook(xlsFile)
    sheet = workbook.sheet_by_index(0)

    file = open(csvFile, "wb")
    csvOutput = unicodecsv.writer(file, encoding='utf-8')

    for row in xrange(sheet.nrows):
        csvOutput.writerow(sheet.row_values(row))
    file.close()

with open('input.txt', 'r') as f:
	lines = f.readlines()

with open('output.txt', 'w+') as g:
	for line in lines:
		if sys.argv[1] == 'fingerhut':
			if len(line) > 4:
				url = ('http://www.fingerhut.com/product/%s.uts' % line[1:6])
				title = (line[13:-1])
				title2 = title.rstrip()
				title3 = title2.lstrip()
				title3.replace('"', 'inch').replace('"', 'inch', 10).replace("'", 'inch').replace(')', '')
				g.write('=HYPERLINK("%s;%s")\n' % (url, title3))
				#print url
			else:
				 g.write('\n')

		elif sys.argv[1] == 'sportsman':
			staticurl = "http://www.sportsmansguide.com"
			if len(line) > 2:
				productid = line[0:6]
				response = br.open(staticurl)
				br.select_form(nr = 2 )
				br.form['k'] = productid
				response2 = br.submit()
				url = response2.geturl()
				
				line1 = line.replace('/t', '')
				line2 = line1.replace('/n', '')
				line3 = line2.replace('/r', '')
				title = line2[7:-1]
				g.write('=HYPERLINK("%s;%s")\n' % (url, title))

			else:
	 			g.write('/n')

		elif sys.argv[1] == 'shophq':
			if len(line) > 2:
				#url = ('http://www.shophq.com/offer/default.aspx?offercode='  + line[0:7] )
				url = ('http://www.evine.com/Product/%s' % line[0:7])
				title = (line[9:-1])

				title2 = title.rstrip()
				title3 = title2.lstrip()
				title3.replace('"', 'inch').replace('"', 'inch', 10).replace("'", 'inch')
						
				title3.replace(')', '')
				g.write('=HYPERLINK("%s;%s")\n' % (url, title3))
			
			else:
				g.write('\n')
							
		elif sys.argv[1] == 'amazon':
			if len(line) > 2:
				url = ('https://www.amazon.com/dp/%s' % line[0:10])
				title = (line[13:-1])

				title2 = title.rstrip()
				title3 = title2.lstrip()
				title3.replace('"', 'inch').replace('"', 'inch', 10).replace("'", 'inch').replace(')', '')
				g.write('=HYPERLINK("%s;%s")\n' % (url, title3))
			
			else:
				g.write('\n')

		elif sys.argv[1] == 'stoneberry':
			if len(line) > 4:
				SKU = line.split('\t')[0]
				sku1, sku2 = SKU.split('-')
				#print SKU
				title=line.split('\t')[1]
				url = ("https://www.stoneberry.com/product/%s-%s?Ntt=%s" % (sku1, sku2, SKU))
				#url = ("https://www.stoneberry.com/product/" + str(SKU.split('-')[0]) + "-" + str(SKU.split('-')[1]) + "?Ntt=" + str(SKU) )

				title2 = title.rstrip()
				title3 = title2.lstrip()
				title3.replace('"', 'inch').replace('"', 'inch', 10).replace("'", 'inch').replace(')', '')
				g.write('=HYPERLINK("%s;%s")\n' % (url, title3))
		else:
			g.write('\n')
