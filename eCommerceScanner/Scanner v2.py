import json, csv, os
import Tkinter as tk
from datetime import datetime

fullArray = []

opj = os.path.join
timestamp = 'ScanLog-%s' % datetime.now().strftime('%I.%M.%S%p')
daystamp = datetime.now().strftime('%m-%d-%Y')
folderWithTodaysDate = opj('%s\Logs\\' % os.getcwd(), daystamp)
header = ['PALLET', 'ITEM', 'VARIATION', 'BARCODE', 'DEPARTMENT', 'DESCRIPTION', 'RETAIL']#, 'QTY']

def center(toplevel): # Function for centering all windows upon execution.
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth() #Find width resolution
    h = toplevel.winfo_screenheight() #Find height resolution
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2 # find the middle of width resolution
    y = h/2 - size[1]/2 # find the middle of height resolution
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))	

def makeFolder():
	if os.path.exists(folderWithTodaysDate) == True: #If file w/ today's date exists, then continue the script.
		pass
	else:
		os.makedirs(folderWithTodaysDate, 0666) #read/write permissions for creating files inside python created folder. For Win & Linux.

def runLog(fullArray):
	with open(opj(folderWithTodaysDate, 'EmergencyRecovery.txt'), 'w+') as log:
		log.write('%s\n' % header)
		log.write('%s\n' % fullArray)
	log.close()

def outputLog(fullArray):
	with open('%s.csv' % opj(folderWithTodaysDate, timestamp), 'w+') as manifest:
		writer = csv.writer(manifest, delimiter=',', lineterminator='\n')
		writer.writerow(header)
		for row in fullArray:
			writer.writerow(row)
	manifest.close()

def delete():
	try:
		fullArray.pop()
	except:
		print 'Array Empty'
	finally:
		history()

def getProductDetails(scan):
	scan = str(scan)
	with open('shoesLookup.json', 'r') as jf:
		data = json.load(jf)

	cids = [i for i in data]

	if scan in cids:
		desc = data[scan][0]['Item Description']
		dept = data[scan][0]['Department Name']
		retail = data[scan][0]['Retail']
		matches = [desc, dept, retail]
		return matches

def descHistory():
	try:
		HistoryDesc0 = tk.Label(width=18, anchor='n', relief='ridge', fg='blue', text='%s' % fullArray[-1][4])
		HistoryDesc0.grid(row=6, column=1, padx=(110,5), pady=5)
	except:
		HistoryDesc0 = tk.Label(width=18, anchor='n', relief='ridge', fg='red', text='ATTN! %s' % fullArray[-1][3])
		HistoryDesc0.grid(row=6, column=1, padx=(110,5), pady=5)

def history():
	x = len(fullArray)
	last = x-1

	print x

	HistoryCID0 = tk.Label(width=15, anchor='n', relief='ridge', text='')
	HistoryCID0.grid(row=6, column=0, padx=5, pady=5)
	HistoryVar0 = tk.Label(width=20, anchor='n', relief='ridge', text='')
	HistoryVar0.grid(row=6, column=1, padx=(5,195), pady=5)
	HistoryDesc0 = tk.Label(width=18, anchor='n', relief='ridge', text='')
	HistoryDesc0.grid(row=6, column=1, padx=(110,5), pady=5)
	HistoryCounter0 = tk.Label(width=5, anchor='n', relief='ridge', text='')
	HistoryCounter0.grid(row=6, column=1, padx=(300, 5), pady=5)

	HistoryCID1 = tk.Label(width=15, anchor='n', relief='ridge', text='')
	HistoryCID1.grid(row=7, column=0, padx=5, pady=5)
	HistoryVar1 = tk.Label(width=20, anchor='n', relief='ridge', text='')
	HistoryVar1.grid(row=7, column=1, padx=(5,195), pady=5)
	HistoryDesc1 = tk.Label(width=18, anchor='n', relief='ridge', text='')
	HistoryDesc1.grid(row=7, column=1, padx=(110,5), pady=5)
	HistoryCounter1 = tk.Label(width=5, anchor='n', relief='ridge', text='')
	HistoryCounter1.grid(row=7, column=1, padx=(300, 5), pady=5)

	try:
		HistoryCID0 = tk.Label(width=15, anchor='n', relief='ridge', text='%s' % fullArray[-1][1])
		HistoryCID0.grid(row=6, column=0, padx=5, pady=5)
		HistoryVar0 = tk.Label(width=20, anchor='n', relief='ridge', text='%s' % fullArray[-1][2])
		HistoryVar0.grid(row=6, column=1, padx=(5,195), pady=5)	

		HistoryCounter0 = tk.Label(width=5, anchor='n', relief='ridge', text='')
		HistoryCounter0.grid(row=6, column=1, padx=(300, 5), pady=5)
		try:
			HistoryCID1 = tk.Label(width=15, anchor='n', relief='ridge', text='%s' % fullArray[-2][1])
			HistoryCID1.grid(row=7, column=0, padx=5, pady=5)
			HistoryVar1 = tk.Label(width=20, anchor='n', relief='ridge', text='%s' % fullArray[-2][2])
			HistoryVar1.grid(row=7, column=1, padx=(5,195), pady=5)
			descHistory()
			try:
				HistoryDesc1 = tk.Label(width=18, anchor='n', relief='ridge', fg='blue', text='%s' % fullArray[-2][4])
				HistoryDesc1.grid(row=7, column=1, padx=(110,5), pady=5)
				
				HistoryCounter1 = tk.Label(width=5, anchor='n', relief='ridge', text='')
				HistoryCounter1.grid(row=7, column=1, padx=(300, 5), pady=5)
						
			except:
				HistoryDesc1 = tk.Label(width=18, anchor='n', relief='ridge', fg='red', text='ATTN! %s' % fullArray[-2][3])
				HistoryDesc1.grid(row=7, column=1, padx=(110,5), pady=5)
				
				HistoryCounter1 = tk.Label(width=5, anchor='n', relief='ridge', text='')
				HistoryCounter1.grid(row=7, column=1, padx=(300, 5), pady=5)
		except:
			descHistory()
	except:
		pass

def GetStaticInputs(endUserInputs):
	tempArray = []

	for each in endUserInputs:
		tempArray.append(str(each.get()))
	pallet, costcoID, variation, barcode = [i.get() for i in endUserInputs]
	
	try:
		matchArray = []
		[matchArray.append(m) for m in getProductDetails(costcoID)]

		for each in matchArray:
			tempArray.append(each)
		fullArray.append(tempArray)

	except:
		fullArray.append(tempArray) # append array with manual inputs, regardless of CID being found in dbase.

	finally:
		history()
		outputLog(fullArray)
		runLog(fullArray)

class MainApp(tk.Tk): # Main GUI window with buttons in line.
	def __init__(self):
		tk.Tk.__init__(self)

		LoadIDLabel = tk.Label(width=15, relief='ridge',text='Pallet')#header[0])
		LoadIDLabel.grid(row=0, column=0, padx=5, pady=5)
		ExternalIDLabel = tk.Label(width=15, relief='ridge', text='CID')#header[1])
		ExternalIDLabel.grid(row=1, column=0, padx=5, pady=5)
		VariationLabel = tk.Label(width=15, relief='ridge', text='Variation')#header[2])
		VariationLabel.grid(row=2, column=0, padx=5, pady=5)
		BarcodeLabel = tk.Label(width=15, relief='ridge', text='Barcode')#header[3])
		BarcodeLabel.grid(row=3, column=0, padx=5, pady=5)

		history()

		LoadIDEntry = tk.Entry(width=55)
		LoadIDEntry.grid(row=0, column=1, padx=5, pady=5)
		LoadIDEntry.focus_set()
		ExternalIDEntry = tk.Entry(width=55)
		ExternalIDEntry.grid(row=1, column=1, padx=5, pady=5)
		VariationEntry = tk.Entry(width=55)
		VariationEntry.grid(row=2, column=1, padx=5, pady=5)
		BarcodeEntry = tk.Entry(width=55) #ConditionEntry = tk.Entry(width=55)
		BarcodeEntry.grid(row=3, column=1, padx=5, pady=5) #ConditionEntry.grid(row=4, column=1, padx=5, pady=5)
		
		endUserInputs = [LoadIDEntry, ExternalIDEntry, VariationEntry, BarcodeEntry]#, ConditionEntry]

		EnterButton = tk.Button(text="Enter", width=31, height=2, command=lambda: [GetStaticInputs(endUserInputs), BarcodeEntry.delete(0, 999)])
		EnterButton.grid(row=8, column=0, padx=(0,233), pady=5, columnspan=2)
		DeleteButton = tk.Button(text="Delete", width=31, height=2, command=lambda: delete())
		DeleteButton.grid(row=8, column=1, padx=(110,0), pady=5, columnspan=2)
		self.bind('<Return>', (lambda event: [GetStaticInputs(endUserInputs), BarcodeEntry.delete(0, 999)]))#GetStaticInputs(endUserInputs)))
		self.bind('<Delete>', (lambda event: delete()))
		self.bind('<Key-Escape>', (lambda event: self.destroy()))


if __name__ == "__main__": # compile the main class/widgets to be displayed on screen.
	makeFolder()
	root = MainApp()
	center(root)
	root.resizable(0,0)
	#root.wm_iconbitmap('.\sglogo2.ico')
	root.title('Secret Sauce v2.0')
	root.mainloop()
