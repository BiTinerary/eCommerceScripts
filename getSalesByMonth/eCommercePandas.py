import pandas as pd
from datetime import datetime
import sys, os

try:
	keyword = sys.argv[1] # Pass variable via CLI to change keyword of sales per product
except:
	keyword = 'Luminara' # By default find sales for any item with "Luminara" in item-description/name

exportFolder = './export/' # File filtering, not yet utilized. Export = perform on these spreadsheets 
outputFolder = './output/' # Not yet utilized. Output new standardized spreadsheets (date-range.csv)

def outputLogFile(store, df):
	with open('log.txt', 'a') as log:
		log.write('%s %s\n%s\n----\n\n' % (store, datetime.now().strftime('%m-%d-%y'), df))

def parseExtensionFrom(file): # Determine file type, read as pandas DataFrame correctly.

	if file.endswith('.xlsx'): # If excel file, ie: default Walmart sales export
		print('EXCEL: %s\nWalmart Sales:\n' % file)
		df = pd.read_excel(file)
		#walmartMonthlySales(df, keyword)#.to_csv('%sWalmart Monthly Sales - %s.csv' % (outputFolder, keyword))
		outputLogFile('Walmart', walmartMonthlySales(df, keyword))

	elif file.endswith('.csv'): # If csv file, ie: default Ebay sales export
		print('CSV: %s\neBay Sales:\n' % file)
		df = pd.read_csv(file, encoding='cp1252')
		#ebayMonthlySales(df, keyword)#.to_csv('%sEbay Monthly Sales - %s.csv' % (outputFolder, keyword))
		outputLogFile('Ebay', ebayMonthlySales(df, keyword))

	elif file.endswith('.txt'): # If tabulated .txt file, ie: Default Amazon sales export.
		print('TXT: %s\nAmazon Sales:\n' % file)
		df = pd.read_table(file, encoding='cp1252')
		#amazonSales(df, keyword)#.to_csv('%sAmazon Monthly Sales - %s.csv' % (outputFolder, keyword))
		outputLogFile('Amazon', amazonSales(df, keyword))

# Using headers of eBay 'Paid and Shipped' file exchange Export... My Ebay >> Selling >> File Exchange >> Download Files >> Paid And Shipped.
def ebayMonthlySales(df, keyword): # ...Output monthly sales of a specific product sold on Walmart merketplace
	df['Month'] = [datetime.strptime(i.strip(), '%b-%d-%y') for i in df['Sale Date']] # Assign new standardized 'Month' column by string formatting date of default export
	sales = df['Sale Price'].apply(lambda x: x.strip('$').replace(' ', '').replace('\n', '').replace(',', '')) # Apply lambda function of replacing dollar sign, commas, etc... from sales column.
	values = sales.astype(float) * df['Quantity'] # Multiple quantity of line item, by the sales price float, above.

	df['%s-Boolean' % keyword] = df['Item Title'].str.contains(keyword) # If item title/description contains product keyword, assign true/false boolean column
	df['4PK'] = df['Item Title'].str.contains('%s %s' % (keyword, [pack for pack in ['4"', '6"', '8"']])) # make new boolean column if Item Title contains keyword + 4", 6" or 8".

	df['Total Paid'] = values.where(df['%s-Boolean' % keyword] == True) # New column contains cells of total paid (Sales * Quantity) if product boolean column is True.
	df['%s-Qty' % keyword] = df['Quantity'].where(df['%s-Boolean' % keyword] == True) # New column contains cells of total paid (Sales * Quantity) if product boolean column is True.	
	df['4PK-QTY'] = df['%s-Qty' % keyword].where(df['4PK'] == True)

	onlyGoods = [col for col in df.columns if col in ['Item Title', 'Custom Label', 'Total Paid', 'Month', 'Sale Price', '%s-Qty' % keyword, '4PK-QTY']]
	df2 = df[onlyGoods] # This new dataframe contains only the columns specified above, trim all the extraneous columns from Marketplace default export.

	salesByMonth = df2.groupby([df2['Month'].dt.strftime('%b %Y')], sort=True).sum() # Group by monthly notation, format them for 'pretty print' below.
	salesByMonth['Lanterns'] = salesByMonth['Luminara-Qty'] - salesByMonth['4PK-QTY']

	print('%s\n' % salesByMonth)
	return salesByMonth

#Using headers of Amazon Sales Export... Order Report: Orders >> Order Reports or 'Sold Listing Report': Inventory >> Inventory Reports >> Sold Listings Report
def amazonSales(df, keyword): # ...Output monthly sales of a specific product
	df['Month'] = [i.split()[0] for i in df['purchase-date']]

	try:
		#if sys.argv[2] == 'annual': # Personally use Order Reports as master, Annual sales spreadsheet.
		values = df['item-price']
		df['%s-Boolean' % keyword] = df['product-name'].str.contains(keyword)
		df['4PK'] = df['item-name'].str.contains('%s %s' % (keyword, [pack for pack in ['4"', '6"', '8"']])) # make new boolean column if Item Title contains keyword + 4", 6" or 8".
	except: # If not 'Order Report (annual spreadsheet) headers, default to 'Sold Listings Report' headers.
		values = df['price'] * df['quantity']
		df['%s-Boolean' % keyword] = df['item-name'].str.contains(keyword)
		df['4PK'] = df['item-name'].str.contains('%s %s' % (keyword, [pack for pack in ['4"', '6"', '8"']])) # make new boolean column if Item Title contains keyword + 4", 6" or 8".
	
	df['Total Paid'] = values.where(df['%s-Boolean' % keyword] == True)
	df['%s-Qty' % keyword] = df['quantity'].where(df['%s-Boolean' % keyword] == True) # New column contains cells of total paid (Sales * Quantity) if product boolean column is True.	
	df['4PK-QTY'] = df['%s-Qty' % keyword].where(df['4PK'] == True)

	try:
		#if sys.argv[2] == 'annual': #Again, determine the type of Amazon export file based on headers, then define appropriate header names below
		onlyGoods = [col for col in df.columns if col in ['product-name', 'sku', 'item-price', 'purchase-date', 'buyer-name', 'Total Paid', 'Month', '%s-Qty' % keyword, '4PK-QTY']]

	except:
		onlyGoods = [col for col in df.columns if col in ['item-name', 'sku', 'price', 'purchase-date', 'buyer-nick-name', 'Total Paid', 'Month', '%s-Qty' % keyword, '4PK-QTY']]
	
	df2 = df[onlyGoods]

	toDateObj = pd.to_datetime(df['Month'])
	salesByMonth = df2.groupby(toDateObj.dt.strftime('%b %Y'), sort=True).sum()
	salesByMonth['Lanterns'] = salesByMonth['Luminara-Qty'] - salesByMonth['4PK-QTY']

	#salesByMonth.to_csv('%sAmazon Monthly Sales - %s.csv' % (outputFolder, keyword))
	print('%s\n' % salesByMonth)

	return salesByMonth

#Using headers of Walmart Sales Export... Order Management >> *Click* Dashboard >> Past Orders >> *Click View* Orders >> *Click* Download >> Export All Items
def walmartMonthlySales(df, keyword): # ...Output monthly sales of a specific product
	df['Month'] = [datetime.strptime(i.strip(), '%Y-%m-%d') for i in df['Order Date']]

	df['%s-Boolean' % keyword] = df['Item Description'].str.contains(keyword)
	df['4PK'] = df['Item Description'].str.contains('%s %s' % (keyword, [pack for pack in ['4"', '6"', '8"']])) # make new boolean column if Item Title contains keyword + 4", 6" or 8".

	df['Total Paid'] = df['Item Cost'].where(df['%s-Boolean' % keyword] == True)
	df['%s-Qty' % keyword] = df['Qty'].where(df['%s-Boolean' % keyword] == True) # New column contains cells of total paid (Sales * Quantity) if product boolean column is True.	
	df['4PK-QTY'] = df['%s-Qty' % keyword].where(df['4PK'] == True)

	onlyGoods = [col for col in df.columns if col in ['Order Date', 'Customer Name', 'Item Description', 'SKU', 'Total Paid', '%s-Qty' % keyword, '4PK-QTY']]
	df2 = df[onlyGoods]
	
	salesByMonth = df2.groupby(df['Month'].dt.strftime('%b %Y'), sort=False).sum()
	salesByMonth['Lanterns'] = salesByMonth['Luminara-Qty'] - salesByMonth['4PK-QTY']

	print('%s\n' % salesByMonth)
	return salesByMonth

currentDirectory = next(os.walk('%s' % exportFolder))[2] # list of each file in cwd
for file in currentDirectory:
	if file.endswith(('.txt', 'csv', 'xlsx')):
		parseExtensionFrom('%s%s' % (exportFolder, file))
	else:
		print('\nInput file Format is not recognized!')
		print('Ignoring file: %s\n' % file)
		pass
