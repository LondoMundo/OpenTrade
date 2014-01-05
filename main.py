import wx
import urllib

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
        static = wx.StaticText(panel, -1 ,variable)

        f = open('stocks.txt', 'r')
        tickers = f.readlines()
        print tickers
        static.SetLabel(tickers[0] + tickers[1])

        update = wx.Button(panel, label = "update", pos = (260, 70))
        self.Bind(wx.EVT_BUTTON, self.update, update)

    def TrackStock(self, event):

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
        static.SetLabel("Woah!")

if __name__ == '__main__':
    app=wx.PySimpleApp()
    frame=Main(parent = None, id = -1)
    frame.Show()
    app.MainLoop()
