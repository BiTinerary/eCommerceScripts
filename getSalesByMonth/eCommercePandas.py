import pandas as pd
from datetime import datetime
import sys, os

#try:
#	keyword = sys.argv[1]
#except:
#	keyword = 'Luminara'
#keyword = sys.argv[1]

keyword = 'Luminara'
exportFolder = './export/'
outputFolder = './output/'

def parseExtensionFrom(file): # Input file, output file

	#try:
	#	annual = sys.argv[2]
	#	
	#	annualRead(df, keyword)
	#except:
	# the following

	if file.endswith('.xlsx'):
		print 'EXCEL: %s' % file
		df = pd.read_excel(file)
		walmartMonthlySales(df, keyword)

	elif file.endswith('.csv'):
		print 'CSV: %s' % file
		df = pd.read_csv(file)
		ebayMonthlySales(df, keyword)

	elif file.endswith('.txt'):
		print 'TXT: %s' % file
		df = pd.read_table(file)
		amazonMonthlySales(df, keyword)

def ebayMonthlySales(df, keyword):
	df['Month'] = [datetime.strptime(i.strip(), '%b-%d-%y') for i in df['Sale Date']]
	sales = df['Sale Price'].apply(lambda x: x.strip('$').replace(' ', '').replace('\n', '').replace(',', ''))
	values = sales.astype(float) * df['Quantity']

	df['LummieBool'] = df['Item Title'].str.contains(keyword)
	df['Total Paid'] = values.where(df['LummieBool'] == True)

	onlyGoods = [col for col in df.columns if col in ['Sales Record Number', 'Item Title', 'Quantity', 'Custom Label', 'LummieBool', 'Total Paid', 'Month', 'Sale Price']]
	df2 = df[onlyGoods]

	salesByMonth = df2.groupby([df2['Month'].dt.strftime('%b %Y')], sort=False).sum() #.reset_index()
	print salesByMonth

def walmartMonthlySales(df, keyword):
	df['Month'] = [datetime.strptime(i.strip(), '%Y-%m-%d') for i in df['Order Date']]

	df['LummieBool'] = df['Item Description'].str.contains(keyword)	
	df['Total Paid'] = df['Item Cost'].where(df['LummieBool'] == True)

	onlyGoods = [col for col in df.columns if col in ['PO#', 'Order#', 'Order Date', 'Customer Name', 'Item Description', 'Qty', 'SKU', 'Item Cost', 'Total Paid', 'Tax']]
	df2 = df[onlyGoods]
	
	saleByMonth = df2.groupby(df['Month'].dt.strftime('%b %Y'), sort=False).sum()
	print saleByMonth

def amazonMonthlySales(df, keyword):
	df['Month'] = [i.split()[0] for i in df['purchase-date']]
	values = df['price'] * df['quantity']

	df['LummieBool'] = df['item-name'].str.contains(keyword)
	df['Total Paid'] = values.where(df['LummieBool'] == True)

	onlyGoods = [col for col in df.columns if col in ['item-name', 'sku', 'price', 'purchase-date', 'buyer-nick-name', 'LummieBool', 'Total Paid', 'Month']]
	df2 = df[onlyGoods]

	toDateObj = pd.to_datetime(df['Month'])
	salesByMonth = df2.groupby(toDateObj.dt.strftime('%b %Y'), sort=False).sum()
	print salesByMonth

currentDirectory = next(os.walk('%s' % './'))[2] # Get each spreadsheet filename
for file in currentDirectory:
	if file.endswith(('.txt', 'csv', 'xlsx')):
		parseExtensionFrom(file)
	
	else:
		print '\nInput file Format is not recognized!'
		print 'Ignoring file: %s\n' % file
		pass

#df = pd.read_excel('%s%s' % (spreadName, '.xlsx'))
#df = pd.read_csv('%s%s' % (spreadName, '.csv'))# sys.argv[1])
#df = pd.read_table('%s%s' % (spreadName, '.txt'))
#amazonMonthlySales(df, 'Luminara')
#walmartMonthlySales(df, 'Luminara')
#ebayMonthlySales(df, 'Luminara')
#parseBasedOn(spreadName)
