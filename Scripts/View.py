import tkinter as tk

class View:
    def __init__(self):
        self.window = tk.Tk()
        self.butlerMessage = tk.StringVar()
        self.butlerMessageBox = tk.Message(textvariable=self.butlerMessage)
        self.butlerMessageBox.pack(pady=1)

    def run(self):
        self.window.mainloop()

    #指定秒ごとに関数を実行する。maxRoopCountが-1なら無限ループ
    @staticmethod
    def SetRoop(self, function, period, cancel, maxRoopCount=-1):
        if maxRoopCount == 0:
            return

        self.window.after(period*1000, function)

        if cancel.canceled == True:
            return

        maxRoopCount -= 1

        self.SetRoop(function, period, cancel, maxRoopCount)


    def ShowMessageOneByOne(self, message, period, cancel, count=0):
        if len(message) <= count:
            self.ShowMessage(message)
            cancel.cancel()
            return

        if cancel.canceled == True:
            self.ShowMessage(message)
            return

        self.ShowMessage(message[:count+1])

        args = {"message":message, "period":period, "cancel":cancel,"count":count+1}

        afterId = self.window.after(period*1000, self.ShowMessageOneByOne, args)
        cancel.setId(self.window, afterId)


    def ShowMessageOneByOne(self, message, period, cancel, startCount=0):
        if len(message) <= startCount:
            self.ShowMessage(message)
            cancel.cancel()
            return

        if cancel.canceled == True:
            self.ShowMessage(message)
            return

        self.ShowMessage(message[:startCount+1])

        #nextkwords = {"message":kwords["message"], "period":kwords["period"], "cancel":kwords["cancel"]}

        afterId = self.window.after(int(period*1000), self.ShowMessageOneByOne, message, period, cancel, startCount+1)
        cancel.setId(self.window, afterId)


    def ShowMessage(self, message):
        self.butlerMessage.set(message)