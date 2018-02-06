import csv, glob, os, sys

pwd = os.getcwd()
glob = glob.glob('*.csv')[0]

file = "%s\%s" % (pwd, str(glob))

outputArray = []

if sys.argv[1] == "sales":
	salesAnalysis = [9, 21, 48, 63, 64, 68, 75, 88, 89, 90, 96] # Sales Analysis > Export ShipStation Records + True Shipping cost]
	outputFileName = 'SalesAnalysis.csv'
	theGoodColumns = salesAnalysis

elif sys.argv[1] == "returns":
	returnsAndReplacements = [8, 9, 15, 17, 18, 21, 56, 63, 88, 89, 95, 105] # Monitor returns/replacements. Shipstation > Export all Manual orders.
	outputFileName = "ReturnsAnalysis.csv"
	theGoodColumns = returnsAndReplacements

with open(file, 'r') as inCsv: # input hella long spreadsheet (Shipstation export = 100+ columns)
	content = csv.reader(inCsv, delimiter=',')
	header = content.next() # Headers
	x = 1

	head = []
	for each in theGoodColumns:
		head.append(header[each])
	outputArray.append(head)

	for index in content: # For every row in csv, do the following
		row = [] # Scratch pad array for retaining only desired info/rows
		for each in theGoodColumns: # For each specified index, do the following.
			row.append(index[each]) # Append scratch pad array
		outputArray.append(row) # Append static, master array with entire row
		x += 1
	#print outputArray # Print completed row

with open(outputFileName, 'wb') as outputCsv: # WB because Windows appends /r/n's like an idiot.
	writer = csv.writer(outputCsv) # To write pythonic arrays as comma delimited csv's
	writer.writerows(outputArray) # Write each row without array bracket and quote characters.
	outputCsv.write(',=SUM(B2:B%s),,,,,,,,,,' % x)

#[9, 21, 48, 63, 64, 68, 75, 88, 89, 90, 96] # Sales Analysis > Export ShipStation Records + True Shipping cost]
#CARRIER: 8, CARRIERFEE: 9, CREATEDDATE:15, DELIVERED: 17, DELIVERYDATE: 18, DESCRIPTION:21, NAME:56, ORDERNUMBER:63, SKU:88, STATE:89, TRACKING:95, BATCH#:105

#[8, 9, 15, 17, 18, 21, 56, 63, 88, 89, 95, 105] # Order Analysis > Export all manual orders
#CARRIERFEE:9, DESCRIPTION:21, ITEMS:48, ORDER#:63, ORDERTOTAL: 64, PAYDATE:68, QTY:75,  SKU: 88, STATE: 89 STORE:90, UNITPRICE:96