import requests
from bs4 import BeautifulSoup
from datetime import datetime

analystRatingNotFound = 0
peNotFound = 0
psNotFound = 0
rsi14NotFound = 0

def tickerGetFirst(ticker):
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    ticker = ticker.get() ### retrieves the ticker from the main.py user entry request
    yahoourl = f'https://finance.yahoo.com/quote/{ticker}' ### f string allows for dynamic entry from user, thankfully Yahoo Finance has a simple url search syntax
    r1 = requests.get(yahoourl, headers=headers)
    yahoosoup = BeautifulSoup(r1.text, 'html.parser') ###converts the html to a temporary text file and parses the content
    global companyName ### sets the following variables as global variables so they can be retrieved outside of the def tickerGetFirst call from main.py
    global price  
    global intradayChange
    companyName = yahoosoup.find('h1', {'class': 'D(ib) Fz(18px)'}).text ###parses the url html under the h1 tag for the company name
    price = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text ### parses the url html under the span class for the current company price
    intradayChange = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)'})### parses for the current intraday change value
        ### an if else state was required for intraday change, as the html string of the intradayChange changes depending on whether the stock is up or down for the day. This accounts for that.
    if intradayChange == (None):
        intradayChange = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)'})
    if intradayChange == (None):
        intradayChange = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)'}).text
    elif intradayChange == yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)'}):
        intradayChange = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)'}).text
    else:
        intradayChange = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)'}).text


def peerPE(ticker): ###This function compares the company's PE ratio to the sector's P/E ratio that it operates in.
    global peerPEdifWeight
    global peerPEdifRatio
    global peNotFound
    ticker = ticker.get() ### retrieves the ticker from the main.py user entry request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    finvizurl = f'https://finviz.com/quote.ashx?t={ticker}'
    finvizindustryurl = "https://finviz.com/groups.ashx?g=industry&v=120"
    r2 = requests.get(finvizurl, headers = headers)
    r3 = requests.get(finvizindustryurl, headers = headers)
    finvizsoup = BeautifulSoup(r2.content, 'html.parser')
    finvizindustrysoup = BeautifulSoup(r3.text, 'html.parser')
    try:   ###Some companies will not return a P/E ratio from Finviz, this accounts for that.
        industry = finvizsoup.find('table', {'class': 'fullview-title'}).find_all('tr')[2].td.find_all('a')[1].text
        pe = finvizsoup.find('table', {'class': 'snapshot-table2'}).tr
        pe = float(pe.find_all('td')[3].text) ### Returns the company's PE from Finviz
        peIndustry = float(finvizindustrysoup.find(text=industry).parent.parent.parent.find_all('td')[3].text) ###Finds the industry name of the company inputted, searches on the industry PE url for the name, and returns the industry PE
        peerPEdifRatio = (pe - peIndustry) / peIndustry ###difference between the company PE and the industry PE as a percent of the industry PE
        peerPEdifRatio = round(peerPEdifRatio, 4)
        peerPEdifWeight = None     ###Final product sent to the calculation function
        if peerPEdifRatio < -0.75:     ######this set classifies the resulting ratio into custom weight classes. In this case, lower Price to Earnings ratios give a higher score.
            peerPEdifWeight = 1
        elif -.75 <= peerPEdifRatio < -.59:
            peerPEdifWeight = .9
        elif -.59 <= peerPEdifRatio < -.39:
            peerPEdifWeight = .8
        elif -.39 <= peerPEdifRatio < -.19: ###For example, if a company's P/E is between 39% and 19% lower than the sector average, it's scored a 0.7 out of 1.
            peerPEdifWeight = .7
        elif -.19 <= peerPEdifRatio < 0:
            peerPEdifWeight = .6
        elif 0 <= peerPEdifRatio < .19:
            peerPEdifWeight = .5
        elif .19 <= peerPEdifRatio < .39:
            peerPEdifWeight = .4
        elif .39 <= peerPEdifRatio < .59:
            peerPEdifWeight = .3
        elif .59 <= peerPEdifRatio < .80:
            peerPEdifWeight = .2
        elif .80 <= peerPEdifRatio < 1.0:
            peerPEdifWeight = .1
        elif peerPEdifRatio >= 1.00:
            peerPEdifWeight = 0
        peNotFound = 0
    except Exception as e:
        peNotFound = 1
        
def peerPEcheck(click): ###the "click" variable is taken in from main.py as a boolean based on the status of the relevant check button. If the button is on, this is set to "True," and the isclicked variable is set to 1.
    global peerPEisclicked
    peerPEisclicked = 0  
    if peNotFound == 0: ###Checks that pe was found and is a float variable. If it is not, and a string is returned, the the function returns the isclicked as a 0 and proceeds without that variable.
        if click == False:
            peerPEisclicked = 0
        else:
            peerPEisclicked = 1

    else:
        peerPEisclicked = 0
    
    
def peerPS(ticker):
    ticker = ticker.get() ### retrieves the ticker from the main.py user entry request
    global peerPSdifWeight
    global peerPSdifRatio
    global psNotFound
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    finvizurl = f'https://finviz.com/quote.ashx?t={ticker}'
    finvizindustryurl = "https://finviz.com/groups.ashx?g=industry&v=120"
    r2 = requests.get(finvizurl, headers = headers)
    r3 = requests.get(finvizindustryurl, headers = headers)
    finvizsoup = BeautifulSoup(r2.content, 'html.parser')
    finvizindustrysoup = BeautifulSoup(r3.text, 'html.parser')
    try:    ###Some companies will not return a P/S ratio from Finviz, this accounts for that.
        industry = finvizsoup.find('table', {'class': 'fullview-title'}).find_all('tr')[2].td.find_all('a')[1].text
        ps = finvizsoup.find('table', {'class': 'snapshot-table2'}).find_all("tr")[3]
        ps = float(ps.find_all('td')[3].text) 
        psIndustry = float(finvizindustrysoup.find(text=industry).parent.parent.parent.find_all('td')[6].text) ###Finds the industry name of the company inputted, searches on the industry PE url for the name, and returns the industry PE
        peerPSdifRatio = (ps - psIndustry) / psIndustry ###difference between the company PE and the industry PE as a percent of the industry PE
        peerPSdifRatio = round(peerPSdifRatio, 4) ###rounds the final ratio to 2 decimal places
        peerPSdifWeight = None    ###Final product sent to the calculation function
        if peerPSdifRatio < -0.75:  ######this set classifies the resulting ratio into custom weight classes. In this case, lower Price to Sales ratios give a higher score.
            peerPSdifWeight = 1
        elif -.75 <= peerPSdifRatio < -.59:
            peerPSdifWeight = .9
        elif -.59 <= peerPSdifRatio < -.39:
            peerPSdifWeight = .8
        elif -.39 <= peerPSdifRatio < -.19:
            peerPSdifWeight = .7
        elif -.19 <= peerPSdifRatio < 0:
            peerPSdifWeight = .6
        elif 0 <= peerPSdifRatio < .59:
            peerPSdifWeight = .5
        elif .59 <= peerPSdifRatio < .99:
            peerPSdifWeight = .4
        elif .99 <= peerPSdifRatio < 1.5:
            peerPSdifWeight = .3
        elif 1.5 <= peerPSdifRatio < 2.5:
            peerPSdifWeight = .2
        elif 2.5 <= peerPSdifRatio < 5.0: ### the values under P/S are often skewed for companies that are considered "growth" companies and our weighting scale has been made more sensitive to this fact. Lower scores are given for much higher relative P/S ratios.
            peerPSdifWeight = .1
        elif peerPSdifRatio >= 5.0:
            peerPSdifWeight = 0
        psNotFound = 0
    except Exception as e:
        psNotFound = 1


def peerPScheck(click): ###the "click" variable is taken in from main.py as a boolean based on the status of the relevant check button. If the button is on, this is set to "True," and the isclicked variable is set to 1.
    global peerPSisclicked
    peerPSisclicked = 0
    if psNotFound == 0: 
        if click == False:
            peerPSisclicked = 0
        else:
            peerPSisclicked = 1
    else:
        peerPSisclicked = 0


def rsiRating(ticker):
    ticker = ticker.get() ### retrieves the ticker from the main.py user entry request
    global rsi14Weight
    global rsi14
    global rsi14NotFound
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    finvizurl = f'https://finviz.com/quote.ashx?t={ticker}'
    r2 = requests.get(finvizurl, headers = headers)
    finvizsoup = BeautifulSoup(r2.content, 'html.parser')
    try:    ###Some companies will not return a P/S ratio from Finviz, this accounts for that.
        rsi14 = finvizsoup.find('table', {'class': 'snapshot-table2'}).find_all("tr")[8]
        rsi14 = float(rsi14.find_all('td')[9].text) ###Final product retrieved from the webscrape for rsiRating
        round(rsi14, 4)
        rsi14Weight = (100 - rsi14)/100  ###Final product sent to the calculation function
        rsi14NotFound = 0 
    except Exception as e: 
        rsi14NotFound = 1
     
def rsiRatingcheck(click): ###the "click" variable is taken in from main.py as a boolean based on the status of the relevant check button. If the button is on, this is set to "True," and the isclicked variable is set to 1.
    global rsiRatingisclicked
    rsiRatingisclicked = 0
    if rsi14NotFound == 0:
        if click == False:
            rsiRatingisclicked = 0
        else: 
            rsiRatingisclicked = 1
    else:
        rsiRatingisclicked = 0
    
    
def analystRating(ticker):
    ticker = ticker.get() ### retrieves the ticker from the main.py user entry request
    global analystRatingWeight
    global analystAvgRating
    global analystRatingNotFound
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    barchartRatingURL = f'https://www.barchart.com/stocks/quotes/{ticker}/analyst-ratings' 
    r5 = requests.get(barchartRatingURL, headers = headers)
    barchartRatingSoup = BeautifulSoup(r5.text, 'html.parser')
    
    try:
        analystAvgRating = barchartRatingSoup.find(text="Current").parent.parent.parent.find_all('div')[1].find_all('div')[1].text ###Returns a value out of 5 made of an average of analyst ratings from Wall Street.
        analystRatingWeight = (float(analystAvgRating) / 5)   ###Final product sent to the calculation function 
        analystRatingNotFound = 0
    except Exception as e:
        analystRatingNotFound = 1
 
def analystRatingcheck(click): ###the "click" variable is taken in from main.py as a boolean based on the status of the relevant check button. If the button is on, this is set to "True," and the isclicked variable is set to 1.
    global analystRatingisclicked
    analystRatingisclicked = 0 
    if analystRatingNotFound == 0:
        if click == False:
            analystRatingisclicked = 0
        else:
            analystRatingisclicked = 1
    else:
        analystRatingisclicked = 0 


def finalCalc():
    global ConvictionRating
    global numberOfvariablesused
##-----------------------------The "isclicked values are summed to use in a average to creat the final conviction score---------------------------
    numberOfvariablesused = int(analystRatingisclicked + rsiRatingisclicked + peerPSisclicked + peerPEisclicked) 
#####--------------------------This set of logic statements determines what to include in the summed formula (All criteria weights used are added, the sum is then averaged)
    if numberOfvariablesused == 4: 
        CT = (peerPEdifWeight + peerPSdifWeight + rsi14Weight + analystRatingWeight) / 4
    elif numberOfvariablesused == 3:
        if peerPEisclicked == 0:
            CT = (peerPSdifWeight + rsi14Weight + analystRatingWeight) / 3
        elif peerPSisclicked == 0:
            CT = (peerPEdifWeight + rsi14Weight + analystRatingWeight) / 3
        elif rsiRatingisclicked == 0:
            CT = (peerPEdifWeight + peerPSdifWeight + analystRatingWeight) / 3
        elif analystRatingisclicked == 0:
            CT = (peerPEdifWeight + peerPSdifWeight + rsi14Weight ) / 3
    elif numberOfvariablesused == 2:
        if peerPEisclicked == 1:
            if peerPSisclicked == 1:
                CT = (peerPEdifWeight + peerPSdifWeight) / 2
            elif rsiRatingisclicked == 1:
                CT = (peerPEdifWeight + rsi14Weight) / 2
            elif analystRatingisclicked == 1:
                CT = (peerPEdifWeight + analystRatingWeight) / 2
        elif peerPSisclicked == 1:
            if rsiRatingisclicked == 1:
                CT = (peerPSdifWeight + rsi14Weight) / 2
            elif analystRatingisclicked == 1:
                CT = (peerPSdifWeight + analystRatingWeight) / 2
        elif rsiRatingisclicked == 1:
            CT = (rsi14Weight + analystRatingWeight) / 2
    elif numberOfvariablesused == 1:
        if peerPEisclicked == 1:
            CT = (peerPEdifWeight)
        elif peerPSisclicked == 1:
            CT = (peerPSdifWeight)
        elif rsiRatingisclicked == 1:
            CT = (rsi14Weight)
        elif analystRatingisclicked == 1:
            CT = (analystRatingWeight)
    ConvictionRating = round((CT * 100), 4)  # rating will take the final formula total and divide by the numberOfvariableused variable to get the average criteria's rating
  
    
def save():
    now = str(datetime.now())
    f = open("ConvictionSave.txt", "a")
    f.write('\n' + now + '\n') ### if the user created a calcuation variable from a stock, export the ticker, ticker name, and its conviction rating, and a timestamp. each time the button is pressed, 
    f.write(companyName + '\n')
    f.write("Price: " + price + '\n')
    f.write("Conviction Rating: " + str(ConvictionRating) + '\n')
    f.close()