# -*- coding: utf-8 -*-

"""
Authors:
Michael Guinta
Dylan Humble

"""
from tkinter import *
import tkinter
from utilities import *
import utilities as utilities


class Menu:
    def __init__(self, master):
        frame = Frame(master, width=500, height=400)
        frame.pack(expand = 1, fill = X, side = TOP, anchor = N)
        #---------------------Criteria selection--------------------
        self.bbar = Frame(frame, relief = 'sunken', width=600, bd = 4)
        self.bbar.pack(expand = 1, fill = BOTH, side = BOTTOM, pady = 5)
        self.vcb1 = BooleanVar()
        self.vcb2 = BooleanVar()
        self.vcb3 = BooleanVar()
        self.vcb4 = BooleanVar()
        Label(self.bbar, text='Select criteria to consider:').pack(side=LEFT, padx=5)
        self.cbanalyst = Checkbutton(self.bbar, text='Analyst Ratings', variable = self.vcb1, onvalue=True, offvalue=False, command=self.analystRating)
        self.cbanalyst.pack(side=LEFT, padx=5)
        self.cbpeerPE = Checkbutton(self.bbar, text='Peer P/E Rating', variable = self.vcb2, onvalue=True, offvalue=False, command=self.peerPE)
        self.cbpeerPE.pack(side=LEFT, padx=5)
        self.cbpeerPS = Checkbutton(self.bbar, text='Peer P/S Rating', variable = self.vcb3, onvalue=True, offvalue=False, command=self.peerPS)
        self.cbpeerPS.pack(side=LEFT, padx=5)
        self.cbRSI = Checkbutton(self.bbar, text='14-Day Relative Strength Index', variable = self.vcb4, onvalue=True, offvalue=False, command=self.rsiRating)
        self.cbRSI.pack(side=LEFT, padx=5)
        self.bt2 = Button(self.bbar, text = 'Calculate', command = self.criteriaCalc)
        self.bt2.pack(side = RIGHT, padx= 5)
        #--------------------Ticker Entry---------------------------
        self.x = tkinter.Label()
        self.x2 = tkinter.Label()
        self.x3 = tkinter.Label()
        self.t = StringVar()
        self.ef = Frame(frame, bd=2, relief='groove')
        self.lb2 = Label(self.ef, text='Company Ticker Symbol:', font=('bold'))
        self.lb2.pack(side= LEFT)
        self.entry = Entry(self.ef, textvariable = self.t, bg='white') 
        self.bt = Button(self.ef, text = 'Find', command = self.tickerAsk)
        self.entry.pack(side = LEFT, padx = 5)
        self.bt.pack(side = LEFT, padx= 5)
        self.bt2 = Button(self.ef, text = 'Clear', command = self.clearButton)
        self.bt2.pack(side = LEFT, padx= 5)
        self.ef.pack(expand=0, fill=X, pady=5, side = BOTTOM)
        self.x = Label(self.ef, text = "") ##Intraday Change value from tickerAsk.py
        self.x.pack(side= RIGHT, padx = 10)
        self.w = Label(self.ef, text = 'Intraday Change:')
        self.w.pack(side= RIGHT, padx = 4)
        self.x2 = Label(self.ef, text = "") ##Current price value from tickerAsk.py
        self.x2.pack(side= RIGHT, padx = 4)
        self.w2 = Label(self.ef, text = 'Current Price:')
        self.w2.pack(side= RIGHT, padx = 10)
        self.x3 = Label(self.ef, text = "") ##companyName value from tickerAsk.py
        self.x3.pack(side= RIGHT, padx = 4)
        self.w3 = Label(self.ef, text = 'Company Name:')
        self.w3.pack(side= RIGHT, padx = 10)
        #----Status log----------------------------------------------
        self.lf = Frame(frame, bd=2, relief='groove')
        self.lb = Label(self.lf, text='Status:')
        self.listbox = Listbox(self.lf, height=15)
        self.lb.pack(side=TOP, padx=5, fill=Y)
        self.listbox.pack(padx=5, fill = X)
        self.lf.pack(fill="both", expand=1, pady=5, before = self.bbar, side = BOTTOM)
        #Conviction results------------------------------------------
        self.c = StringVar()
        self.cr = Frame(frame, bd=2, relief = 'groove')
        self.cl = Label(self.cr, text = "Conviction Rating: ", font=("Segoe", 20, 'bold'))
        self.entry = Entry(self.cr, textvariable = self.c, font = ("Segoe", 20))
        self.cl.pack(padx=5)
        self.cs = Label(self.cr, text = "", font=("Segoe", 20, 'bold'))
        self.cs.pack(padx=5)
        self.key = Label(self.cr, text = "0-20: Lowest Conviction      20-40: Low Conviction      40-60: Average Conviction      60-80: High Conviction      80-100: Highest Conviction")
        self.key.pack(padx=5)
        self.cr.pack(expand=1, fill=BOTH, pady=5, side = BOTTOM)
        #-----Save Button---------------------------------------------
        self.sf = Frame(frame, bd=1, relief= 'groove')
        self.sf.pack(expand =1, fill='both', pady=5, side=BOTTOM, after=self.lf)
        self.bt3 = Button(self.sf, text="Save current calculation", command = self.saveButton)
        self.bt3.pack(side=BOTTOM, padx=5)
        #-------------------------------------------------------------
    def tickerAsk(self): ##when the user presses "Find" after entering a stock ticker, this function is called, sending the user's input to a webscraper function in utilities.py
          self.listbox.insert(END,'"'+ self.t.get()+'"' + ' Selected')
          try:
               utilities.tickerGetFirst(self.t) #calls the first webscraper def from utilities.py, with the user's entry "self.t" as the call in variable.
               self.x.configure(text = utilities.intradayChange) #sets the intraday change label to what is returned by the data from yahoo finance.
               self.x2.configure(text = "$"+utilities.price) #sets the price label to what is returned by the data from yahoo finance.
               self.x3.configure(text = utilities.companyName) #sets the company name label to what is returned by the data from yahoo finance.
               utilities.analystRating(self.t) ### Re-calls the analyst rating def for use in the finalCalc def in utilities.py
               utilities.peerPE(self.t) ### Re-calls the Peer P/E def for use in the finalCalc def in utilities.py
               utilities.peerPS(self.t) ### Re-calls the Peer P/S def for use in the finalCalc def in utilities.py
               utilities.rsiRating(self.t) ### Re-calls the RSI Rating def for use in the finalCalc def in utilities.py
               if utilities.analystRatingNotFound == 1:
                   self.listbox.insert(END, "Could not find "+ self.t.get() + "'s Analyst Rating")
               if utilities.peNotFound == 1:
                   self.listbox.insert(END, "Could not find "+ self.t.get() + "'s P/E Ratio")
               if utilities.psNotFound == 1:
                   self.listbox.insert(END, "Could not find "+ self.t.get() + "'s P/S Ratio")
               if utilities.rsi14NotFound == 1:
                   self.listbox.insert(END, "Could not find "+ self.t.get() + "'s 14-day RSI")                  
               self.listbox.insert(END, self.t.get() + ' Successfully loaded')
          except Exception as e: #if nothing is returned, the exception returns an error message
               print(e)
               self.listbox.insert(END, 'Error finding all ' + self.t.get()+ " data")

    def clearButton(self): ##update to remove all dynamic variables at the end
        self.x.configure(text = "") ## Sets the descriptive data feed (company, price, intraday change) to ""
        self.x2.configure(text = "")
        self.x3.configure(text = "")
        self.cs.configure(text = "")
        self.vcb1.set(False) ## Sets the criteria check buttons to off
        self.vcb2.set(False)
        self.vcb3.set(False)
        self.vcb4.set(False)
        self.listbox.delete(0, END) ## clears the listbox
        self.listbox.insert(END, 'Search Cleared')
        
    def analystRating(self):
        utilities.analystRatingcheck(self.vcb1) ###clicking the check button changes the boolean's state, calls the check def, and changes the analystRatingisclicked variable.
        self.listbox.insert(END, 'Changed Analyst Rating setting ')   
        
    def peerPE(self):
        utilities.peerPEcheck(self.vcb2) ###clicking the check button changes the boolean's state, calls the check def, and changes the analystRatingisclicked variable.
        self.listbox.insert(END, 'Changed Peer P/E setting ')

    def peerPS(self):
        utilities.peerPScheck(self.vcb3) ###clicking the check button changes the boolean's state, calls the check def, and changes the analystRatingisclicked variable.
        self.listbox.insert(END, 'Changed Peer P/S setting ')
        
    def rsiRating(self):
        utilities.analystRatingcheck(self.vcb4) ###clicking the check button changes the boolean's state, calls the check def, and changes the analystRatingisclicked variable.
        self.listbox.insert(END, 'Changed RSI(14) setting ')
        
    def criteriaCalc(self):
        self.listbox.insert(END, 'Started Calculation ')
        utilities.analystRatingcheck(self.vcb1.get()) ####this calls the check function in utilities.py with the state of the check button (True or False)
        utilities.peerPEcheck(self.vcb2.get()) ####this calls the check function in utilities.py with the state of the check button (True or False)
        utilities.peerPScheck(self.vcb3.get()) ####this calls the check function in utilities.py with the state of the check button (True or False)
        utilities.rsiRatingcheck(self.vcb4.get()) ####this calls the check function in utilities.py with the state of the check button (True or False)
        utilities.analystRating(self.t) ### Re-calls the analyst rating def for use in the finalCalc def in utilities.py
        utilities.peerPE(self.t) ### Re-calls the Peer P/E def for use in the finalCalc def in utilities.py
        utilities.peerPS(self.t) ### Re-calls the Peer P/S def for use in the finalCalc def in utilities.py
        utilities.rsiRating(self.t) ### Re-calls the RSI Rating def for use in the finalCalc def in utilities.py
        
        if utilities.analystRatingNotFound == 0: ##Checks that this rating is found from the source website
            self.listbox.insert(END, self.t.get() +" has an average analyst rating of " + utilities.analystAvgRating)
        else:   ###this is called when the criteria is unable to be scraped from the source page, prompting the error message and setting change
            self.vcb1.set(False)
            self.listbox.insert(END, "Could not find " + self.t.get() + "'s Analyst Rating")
        if utilities.peNotFound == 0: ##Checks that this rating is found from the source website
            self.listbox.insert(END, self.t.get() + " has a P/E Ratio " + str(utilities.peerPEdifRatio*100) + "% above or below its peers" )
        else:   ###this is called when the criteria is unable to be scraped from the source page, prompting the error message and setting change
            self.vcb2.set(False)
            self.listbox.insert(END, "Could not find " + self.t.get() + "'s P/E Ratio")            
        if utilities.psNotFound == 0: ##Checks that this rating is found from the source website
            self.listbox.insert(END, self.t.get() + " has a P/S Ratio " + str(utilities.peerPSdifRatio*100) + "% above or below its peers" )
        else:   ###this is called when the criteria is unable to be scraped from the source page, prompting the error message and setting change
            self.vcb3.set(False)
            self.listbox.insert(END, "Could not find " + self.t.get() + "'s P/S Ratio")
        if utilities.rsi14NotFound == 0: ##Checks that this rating is found from the source website
            self.listbox.insert(END, self.t.get() + " has a 14-day RSI of " + str(utilities.rsi14))  
        else:   ###this is called when the criteria is unable to be scraped from the source page, prompting the error message and setting change
            self.vcb4.set(False)
            self.listbox.insert(END, "Could not find " + self.t.get() + "'s 14-day RSI")
            
        utilities.finalCalc()
        self.cs.configure(text = utilities.ConvictionRating)
        self.listbox.insert(END, 'Finished Calculation ')                
        
    def saveButton(self):
        try: #if the Conviction Rating label is not "", clicking save will append the new rating, company name, price, and the time it was saved to save.txt. Otherwise, save nothing.
            #########-------------------------This def requires all calculations be re-done to be saved since the original calls all happen outside of this def-------------------
            utilities.analystRatingcheck(self.vcb1.get()) ####this calls the check function in utilities.py with the state of the check button (True or False)
            utilities.peerPEcheck(self.vcb2.get()) ####this calls the check function in utilities.py with the state of the check button (True or False)
            utilities.peerPScheck(self.vcb3.get()) ####this calls the check function in utilities.py with the state of the check button (True or False)
            utilities.rsiRatingcheck(self.vcb4.get()) ####this calls the check function in utilities.py with the state of the check button (True or False)
            utilities.analystRating(self.t) ### Re-calls the analyst rating def for use in the finalCalc def in utilities.py
            utilities.peerPE(self.t) ### Re-calls the Peer P/E def for use in the finalCalc def in utilities.py
            utilities.peerPS(self.t) ### Re-calls the Peer P/S def for use in the finalCalc def in utilities.py
            utilities.rsiRating(self.t) ### Re-calls the RSI Rating def for use in the finalCalc def in utilities.py 
            utilities.finalCalc()
            ###-------------------------------------------------------------------------------------------------------------------------------------------------------------------
            utilities.save() ##Calls the Final save function
            self.listbox.insert(END, 'Saved results ')
        except Exception as e:
            self.listbox.insert(END, 'Cannot save, enter a ticker to find a rating for and calculate to save')


def main():
    root = Tk()
    root.configure(background="white")
    root.geometry("1200x510")
    all = Menu(root)
    root.title('Computational Thinking ~ Stock Ticker Rating Calculator')
    root.pack_propagate(1)
    root.mainloop()

if __name__ == "__main__":
    main()