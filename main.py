import urllib

import wx


class Main(wx.Frame):
    def __init__(self, parent, id):
        variable = "stuff"
        wx.Frame.__init__(self, parent, id, "Stock Tracker")
        panel = wx.Panel(self)
        TrackStock = wx.Button(panel, label = "Add stock to tracker", pos = (260, 0))
        self.Bind(wx.EVT_BUTTON, self.TrackStock, TrackStock)
        GetPrices = wx.Button(panel, label = "Get Prices", pos = (260, 30))
        self.Bind(wx.EVT_BUTTON, self.GetPrices, GetPrices)



        global static
        static = wx.StaticText(panel, -1 ,variable, pos=(0,0), size=(100,200))

        f = open('stocks.txt', 'r')
        tickers = f.readlines()
        i=0
        loop = 1
        global allTickers
        allTickers = ""
        while loop==1:
            try:

                allTickers += tickers[i]
                allTickers += "\n"
                i+=1

            except:

                loop = 2
        static.SetLabel(allTickers)
        f.close()
        global priceUpdate
        def priceUpdate():
            global prices
            prices = wx.StaticText(panel, -1 ,variable, pos=(60,0), size=(100,200))

            f = open('stocks.txt', 'r')
            tickers = f.readlines()
            i=0
            loop = 1
            global priceList
            priceList = ""
            while loop==1:
                try:
                    check = tickers[i]
                    print tickers[i]
                    price = urllib.urlopen("http://finance.yahoo.com/d/quotes.csv?s="+check+"&f=l1")
                    price = price.read()
                    print price

                    priceList += price
                    i+=1
                except:
                    loop = 2
                    print "fail"
            prices.SetLabel(priceList)
        priceUpdate()






        update = wx.Button(panel, label = "update", pos = (260, 70))
        self.Bind(wx.EVT_BUTTON, self.update, update)

    def TrackStock(self, event):
        entry = wx.TextEntryDialog(None, "Enter the symbol of the stock you want to track, All caps", "Stock Tracker")
        #pass entry through toUpper. Never trust the user
        entry = entry.ShowModal()
        toTrack = urllib.urlopen("http://finance.yahoo.com/d/quotes.csv?s=GOOG&f=s")
        out = toTrack.read()
        length = len(out)
        length = length - 3
        out = out[1:length]
        print out
        #open the files to write to
        f = open('stocks.txt', 'r')
        file = f.read()
        f.close()
        f = open('stocks.txt', 'w+')
        final = file + out + "\n"
        f.write(final)
        f.close()

    def GetPrices(self, event):
        f=open('stocks.txt', 'r')
        stocks = f.readlines()
        i = 0
        case = True
        while case == True:
            try:
                #check equals the name of the stock as its symbol
                check = stocks[i]
                priceCheck = urllib.urlopen("http://finance.yahoo.com/d/quotes.csv?s="+check+"&f=l1")
                priceCheck = priceCheck.read()
                print priceCheck

                box=wx.MessageDialog(None, check + "has the price " + priceCheck, 'title')
                answer=box.ShowModal()

                i+=1
                case = True
            except:
                case = False

    def update(self, event):
        priceUpdate()

if __name__ == '__main__':
    app=wx.PySimpleApp()
    frame=Main(parent = None, id = -1)
    frame.Show()
    app.MainLoop()
