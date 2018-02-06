import unicodecsv, xlrd, sys, csv, os, time
from datetime import datetime

currentTime = datetime.now() # One global for current time/month. Used basically everywhere.
curMonth = currentTime.strftime("%m-%Y")

try:
	eCommSKU = '%s' % sys.argv[1]
except:
	eCommSKU = "LUM"

inputFolder = './SpreadsheetExports/' # hardcoded location of input files
outputFolder = './output/' # hardcoded file for output, converted files.

def amazonIndexes(storeName, header, salesLog):
	total = 0
	x = 1

	writeHeader(header, storeName, curMonth)
	writeHeader(header, storeName, 'PrevMonths')

	for index in salesLog:
		if index[2][0:3] != eCommSKU:
			pass

		elif index[2][0:3] == eCommSKU:
			purchaseDate = index[5].split(" ")[0] 
			purchaseDate = datetime.strptime(purchaseDate, '%Y-%m-%d') 

			if currentTime.strftime('%m') == purchaseDate.strftime('%m'): # Match numerical month string in spreadsheet, with current month. ie: 11, 12, etc...
				output = open('%s/%s-%s.csv' % (outputFolder, storeName, currentTime.strftime("%m-%Y")), 'a+')
				x += 1
				total += float(index[3]) * float(index[10])
			
			elif currentTime.strftime('%m') != purchaseDate.strftime('%m'):
				output = open('%s/PrevMonths/%s-PrevMonths.csv' % (outputFolder, storeName), 'a+')

			for each in index:
				output.write('%s,' % each.replace(",", ""))
			print index

			output.write("=sum(D%s*K%s)" % (x, x)) # Amazon has line items, regardless of multi item orders. Multiply 'Quantity' with 'Sale price.'
			output.write('\n') # new line escaped

	output.write(",,,=SUM(D2:D%s),,,,,,,=SUM(K2:K%s),=SUM(L2:L%s)" % (x, x, x))
	output.close()
	totalSalesLog("Amazon: $%s" % total)

def eBayIndexes(storeName, header, salesLog): # Run on ebay Spreadsheet
	total = 0
	x = 1
	
	writeHeader(header, storeName, curMonth)
	writeHeader(header, storeName, 'PrevMonths')

	for index in salesLog:
		if index[31][0:3] != eCommSKU: # index 31 == 'Custom SKU'
			pass # Is not a product we want total sales of

		elif index[31][0:3] == eCommSKU: # Is product we want total sales of
			purchaseDate = index[25]
					
			if purchaseDate != "": # Ebay has some lines (multiple item orders) that are blank. Disclude them.
				purchaseDate = datetime.strptime(purchaseDate, '%b-%d-%y') # make datetime instance using date format string from spreadsheet.
				
				if currentTime.strftime('%b') == purchaseDate.strftime('%b'): # Match month abbreviation to current. ie: Nov, Dec, etc...
					output = open('%s/%s-%s.csv' % (outputFolder, storeName, currentTime.strftime("%m-%Y")), 'a+')
					x += 1
					total += float(index[20].replace("$", ""))

				elif currentTime.strftime('%b') != purchaseDate.strftime('%b'): # If sale not in this month
					output = open('%s/PrevMonths/%s-PrevMonths.csv' % (outputFolder, storeName), 'a+')

				for each in index:
					output.write('%s,' % each.replace(",", ""))
				print index

				output.write('\n')
	
	output.write(",,,,,,,,,,,,,,,=SUM(P2:P%s),,,,,=SUM(U2:U%s),,,,,,,,,,,,,,,,,,,,," % (x, x))
	output.close()
	totalSalesLog("eBay: $%s" % total)

	# Ugly code for last line in csv with spreadsheet functions in their respective columns.

def wallyIndexes(storeName, header, salesLog):
	total = 0
	x = 1

	writeHeader(header, storeName, curMonth)
	writeHeader(header, storeName, 'PrevMonths')

	for index in salesLog:
		if index[20][0:3] != eCommSKU:
			pass

		elif index[20][0:3] == eCommSKU:		
			purchaseDate = index[2]
			purchaseDate = datetime.strptime(purchaseDate, '%Y-%m-%d')

			if currentTime.strftime('%m') == purchaseDate.strftime('%m'):
				output = open('%s/%s-%s.csv' % (outputFolder, storeName, currentTime.strftime("%m-%Y")), 'a+')
				x += 1
				total += float(index[21])

			elif currentTime.strftime('%m') != purchaseDate.strftime('%m'):
				output = open('%s/PrevMonths/%s-PrevMonths.csv' % (outputFolder, storeName), 'a+')

			for each in index:
				output.write('%s,' % each.replace(",", ""))
			print index

			output.write('\n')

	output.write(",,,,,,,,,,,,,,,,,,,=SUM(T2:T%s),,=SUM(V2:V%s),,,,,,,," % (x, x))
	output.close()
	totalSalesLog("Wally: $%s" % total)
	# Ugly code for last line in csv with spreadsheet functions in their respective columns.

def shipStationIndexes(storeName, header, salesLog):
	total = 0
	x = 1

	writeHeader(header, storeName, curMonth)
	writeHeader(header, storeName, 'PrevMonths')

	for index in salesLog:
		if index[88][0:3] != 'LUM':
			pass

		elif index[88][0:3] == eCommSKU:
			purchaseDate = index[68].split(" ")[0]
			purchaseDate = datetime.strptime(purchaseDate, '%m/%d/%Y')

			if currentTime.strftime('%m') == purchaseDate.strftime('%m'):
				output = open('%s/%s-%s.csv' % (outputFolder, storeName, currentTime.strftime("%m-%Y")), 'a+')
				x += 1
				total += float(index[96]) * float(index[75])

			elif currentTime.strftime('%m') != purchaseDate.strftime('%m'):
				output = open('%s/PrevMonths/%s-PrevMonths.csv' % (outputFolder, storeName), 'a+')

			for each in index:
				output.write('%s,' % each.replace(",", "")) # replace any rogue commas in product title, customer address, etc...
			print index
				
			output.write("=sum(CS%s*BX%s)" % (x, x))
			output.write('\n')

	output.write(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,=SUM(BX2:BX%s),,,,,,,,,,,,,,,,,,,,,=SUM(CS2:CS%s),,,,,,,,,,=SUM(DC2:DC%s)" % (x, x, x))
	output.close()
	totalSalesLog("ShipStation: $%s" % total)

def parseBasedOn(storeName, header, salesLog): # We quick check which store the spreadsheet belongs to
	if storeName == 'eBay':
		eBayIndexes(storeName, header, salesLog)
	elif storeName == 'Amazon':
		amazonIndexes(storeName, header, salesLog)
	elif storeName == 'Wally':
		wallyIndexes(storeName, header, salesLog)
	elif storeName == 'ShipStation':
		shipStationIndexes(storeName, header, salesLog)

def xls2csv(xlsFile, csvFile): # Kudos to https://www.penwatch.net/cms/excel_to_csv/
    workbook = xlrd.open_workbook(xlsFile)
    sheet = workbook.sheet_by_index(0)

    file = open(csvFile, "wb")
    csvOutput = unicodecsv.writer(file, encoding='utf-8')

    for row in xrange(sheet.nrows):
        csvOutput.writerow(sheet.row_values(row))
    file.close()

def makeFile(file): # Input file, output file
	with open(file, 'r') as inCsv:

		if file.endswith('.txt'):
			salesLog = csv.reader(inCsv, delimiter='\t') # If txt file (Amazon is) tab delimited
			# A little redundant code but necessary for reading header (full spreadsheet) properly later on
		else:
			salesLog = csv.reader(inCsv, delimiter=',')
		
		header = salesLog.next()
		if header[0:3] == ['item-name', 'listing-id', 'sku']: # Amazon header
			storeName = 'Amazon'
		elif header[0:3] == ['Sales Record Number', 'User Id', 'Buyer Fullname']: # Ebay header
			storeName = 'eBay'
		elif header[0:3] == ['PO#', 'Order#', 'Order Date']: # Wally header
			storeName = 'Wally'
		elif header[0:3] == ['AmountPaid', 'BatchID', 'BillDutiesToSender']: # Shipstation header
			storeName = 'ShipStation'

		parseBasedOn(storeName, header, salesLog)

def writeHeader(content, storeName, month):
	if month == 'PrevMonths':
		output = open('%s/PrevMonths/%s-%s.csv' % (outputFolder, storeName, month), 'a+')
	else:
		output = open('%s/%s-%s.csv' % (outputFolder, storeName, month), 'a+') # Output CSV

	for each in content: # Keep original marketplace header intact.
		output.write('%s,' % each) # Comma dlimited
	output.write('\n') # New line escaped

def totalSalesLog(sales):
	with open('totalSales.txt', 'a+') as allSales:
		allSales.write("%s \n" % sales)

def refreshCurDir():
	currentDirectory = next(os.walk('%s' % inputFolder))[2] # Get each spreadsheet filename
	return currentDirectory

with open('totalSales.txt', 'w+') as deleteExistingLog:
	pass

if __name__ == "__main__":
	print refreshCurDir()

	for each in refreshCurDir():
		if each.endswith('.xlsx'):
			xlsFile = '%s%s' % (inputFolder, each)
			csvFile = '%s%s' % (inputFolder, each.replace('.xlsx', '.csv'))
			xls2csv(xlsFile, csvFile)
			os.remove('%s' % xlsFile)

	for eachFile in refreshCurDir(): #Run script on each file
		makeFile('./%s%s' % (inputFolder, eachFile))
