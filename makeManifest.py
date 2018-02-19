import csv
import Tkinter as tk
from Tkinter import IntVar
from datetime import datetime

fullArray = []
outputArray = []

def center(toplevel): # Function for centering all windows upon execution.
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth() #Find width resolution
    h = toplevel.winfo_screenheight() #Find height resolution
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2 # find the middle of width resolution
    y = h/2 - size[1]/2 # find the middle of height resolution
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

class MainApp(tk.Tk): # Main GUI window with buttons in line.
	def __init__(self):
		tk.Tk.__init__(self)

		def eventLog(eventString):
			with open('eachScan.txt', 'a+') as s:
				s.write('%s\n' % eventString)
			s.close()

		def runLog(fullArray):
			with open('CompleteScan.txt', 'w+') as w:
				for each in fullArray:
					w.write('%s\n' % each)
			w.close()

		def outputLog(fullArray):
			with open('ManifestOutput-%s.csv' % datetime.now().strftime('%m-%d-%Y'), 'w+') as manifest:
				writer = csv.writer(manifest, delimiter=',', lineterminator='\n')
				print fullArray
				for row in fullArray:
					print row.split('-')
					#print row.split('-')
					writer.writerow(row.split('-'))

		def delete():
			try:
				fullArray.pop()
				#print fullArray
			except:
				print 'Array Empty'
			finally:
				history()

		def history():
			try:
				HistoryLabel0 = tk.Label(width=65, anchor='n', relief='ridge', text='%s' % fullArray[-1])
				HistoryLabel0.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

				try:
					HistoryLabel1 = tk.Label(width=65, anchor='n', relief='ridge', text='%s' % fullArray[-2])
					HistoryLabel1.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

					try:
						HistoryLabel2 = tk.Label(width=65, anchor='n', relief='ridge', text='%s' % fullArray[-3])
						HistoryLabel2.grid(row=7, column=0, padx=5, pady=5, columnspan=2)
					
					except:
						HistoryLabel2 = tk.Label(width=65, anchor='n', relief='ridge', text='')
						HistoryLabel2.grid(row=7, column=0, padx=5, pady=5, columnspan=2)

				except:
					HistoryLabel1 = tk.Label(width=65, anchor='n', relief='ridge', text='')
					HistoryLabel1.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

			except:
				HistoryLabel0 = tk.Label(width=65, anchor='n', relief='ridge', text='')
				HistoryLabel0.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

		def GetStaticInputs():
			tempArray = []
			getStringArray = [LoadIDEntry, ExternalIDEntry, VariationEntry, BarcodeEntry, ConditionEntry]

			for each in getStringArray:
				tempArray.append(str(each.get()))
			sku = ','.join(tempArray).replace(',', '-').rstrip('-')
			fullArray.append(sku)
			
			outputLog(fullArray)
			runLog(fullArray)
			eventLog(sku)

			history()

		intvar = IntVar()

		header = ['Pallet #', 'External ID:', 'Variation:', 'Barcode:', 'Condition:']

		LoadIDLabel = tk.Label(width=15, relief='ridge',text=header[0])
		LoadIDLabel.grid(row=0, column=0, padx=5, pady=5)

		ExternalIDLabel = tk.Label(width=15, relief='ridge', text=header[1])
		ExternalIDLabel.grid(row=1, column=0, padx=5, pady=5)

		VariationLabel = tk.Label(width=15, relief='ridge', text=header[2])
		VariationLabel.grid(row=2, column=0, padx=5, pady=5)

		BarcodeLabel = tk.Label(width=15, relief='ridge', text=header[3])
		BarcodeLabel.grid(row=3, column=0, padx=5, pady=5)

		ConditionLabel = tk.Label(width=15, relief='ridge', text=header[4])
		ConditionLabel.grid(row=4, column=0, padx=5, pady=5)

		LoadIDEntry = tk.Entry(width=55)
		LoadIDEntry.grid(row=0, column=1, padx=5, pady=5)
		LoadIDEntry.focus_set()

		ExternalIDEntry = tk.Entry(width=55)
		ExternalIDEntry.grid(row=1, column=1, padx=5, pady=5)

		VariationEntry = tk.Entry(width=55)
		VariationEntry.grid(row=2, column=1, padx=5, pady=5)

		BarcodeEntry = tk.Entry(width=55)
		BarcodeEntry.grid(row=3, column=1, padx=5, pady=5)

		ConditionEntry = tk.Entry(width=55)
		ConditionEntry.grid(row=4, column=1, padx=5, pady=5)

		EnterButton = tk.Button(text="Enter", width=31, height=2, command=lambda: GetStaticInputs())
		EnterButton.grid(row=8, column=0, padx=(0,233), pady=5, columnspan=2)

		DeleteButton = tk.Button(text="Delete", width=31, height=2, command=lambda: delete())
		DeleteButton.grid(row=8, column=1, padx=(110,0), pady=5, columnspan=2)

		HistoryLabel0 = tk.Label(width=65, anchor='n', relief='ridge', text='')
		HistoryLabel0.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

		HistoryLabel1 = tk.Label(width=65, anchor='n', relief='ridge', text='')
		HistoryLabel1.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

		HistoryLabel2 = tk.Label(width=65, anchor='n', relief='ridge', text='')
		HistoryLabel2.grid(row=7, column=0, padx=5, pady=5, columnspan=2)

		self.bind('<Return>', (lambda event: GetStaticInputs()))
		#self.bind('<BackSpace>', (lambda event: delete()))
		self.bind('<Delete>', (lambda event: delete()))
		self.bind('<Key-Escape>', (lambda event: self.destroy()))

if __name__ == "__main__": # compile the main class/widgets to be displayed on screen.
	root = MainApp()
	root.resizable(0,0)
	center(root)
	root.title('Operation Secret Sauce')
	root.mainloop()