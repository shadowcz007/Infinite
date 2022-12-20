import wx
import wx.html2
import modules.utils as utils


class MyBrowser(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((800, 900))
        self.SetTransparent(200)
 
if __name__ == '__main__':
    app = wx.App()
    dialog = MyBrowser(None, -1) 
    dialog.browser.LoadURL('http://127.0.0.1:8000/meta-human.html')
    dialog.Show()
    app.MainLoop()
    
