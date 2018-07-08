import os, pandas as pd

exportFolder, scratchFolder, outputFolder, masterFolder = ['./export/', './scratch/', './output/', './Master Annual Sales Reports/']

def diffSpreads(masterDf, convDf, store):
	mastDf = pd.read_csv('{}{}'.format(masterFolder, masterDf), dtype='str')#object, converters={'Buyer Zip': lambda x: str(x)})
	df2 = pd.concat([mastDf, convDf]).drop_duplicates()
	df2.to_csv('{}{}-{}.csv'.format(outputFolder, store, 'NewMaster-DiffMe'), index=False)
	print '{} Converted!'.format(store)

def readMaster(convDf, store):
	for root, dirnames, filenames in os.walk(masterFolder):
		for each in filenames: # Change following 8 lines to [if each.split() == store: diffSpreads(each, convDf, store)]
			if each.split('-')[1] == store:
				diffSpreads(each, convDf, store)

def convertCsv(convFileName, df):
	try:
		df.to_csv('{}'.format(convFileName), index=False)
	except:
		df.to_csv('{}'.format(convFileName), sep=',', encoding='utf-8', index=False)

def parseStoreConvertFile(exportFolder, file): # Determine file type, read as pandas DataFrame correctly.
	curDirFile = '{}{}'.format(exportFolder, file)
	fileName = os.path.basename(file)
	newFileName = os.path.splitext(fileName)[0]

	if file.endswith('.xlsx'): # If excel file, ie: default Walmart sales export
		store = 'Walmart'
		df = pd.read_excel(curDirFile)#, converters={'Buyer Zip': lambda x: str(x)})

		convFileName = '{}CSV-{}-{}.csv'.format(scratchFolder, store, newFileName)
		convertCsv(convFileName, df)
		convDf = pd.read_csv(convFileName, dtype='str')#object, converters={'Buyer Zip': lambda x: str(x)}) #parseConvertedCsv(convFileName)

	elif file.endswith('.csv'): # If csv file, ie: default Ebay sales export
		store = 'Ebay'
		df = pd.read_csv(curDirFile, dtype='str')#object, converters={'Buyer Zip': lambda x: str(x)})
		convFileName = '{}CSV-{}-{}.csv'.format(scratchFolder, store, newFileName)
		convertCsv(convFileName, df)
		convDf = pd.read_csv(convFileName, dtype='str')#object, converters={'Buyer Zip': lambda x: str(x)}) #parseConvertedCsv(convFileName)
		#print convDf

	elif file.endswith('.txt'): # If tabulated .txt file, ie: Default Amazon sales export.
		store = 'Amazon'
		df = pd.read_table(curDirFile, encoding='ISO-8859-1', dtype=object, converters={'Buyer Zip': lambda x: str(x)})

		convFileName = '{}CSV-{}-{}.csv'.format(scratchFolder, store, newFileName)
		convertCsv(convFileName, df)
		convDf = pd.read_csv(convFileName, dtype='str')#object, converters={'Buyer Zip': lambda x: str(x)}) #parseConvertedCsv(convFileName)

	return [convDf, store]

def listSpreadsheets(exportFolder):
	for root, dirnames, filenames in os.walk(exportFolder):
		for file in filenames:
			if file.endswith(('.txt', '.xlsx', '.csv')):
				convDf, store = parseStoreConvertFile(exportFolder, file)
				masterDf = readMaster(convDf, store)
				#print masterDf

listSpreadsheets(exportFolder)