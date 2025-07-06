import tkinter as tk
import CommonView

class View:
    def __init__(self):
        self.window = tk.Tk()

        self.basicFrame = tk.Frame(self.window)
        self.registerFrame = tk.Frame(self.window)
        self.basicFrame.grid(row=0, column=0, sticky="nsew")
        self.registerFrame.grid(row=0, column=0, sticky="nsew")
        self.InitBasicWindow()
        self.InitRegisterWindow()

        self.basicFrame.tkraise()

        self.onShowRegisterWindowButtonClickCallback = []
        self.onRegisterButtonClickCallback = []

    def run(self):
        self.window.mainloop()

    def getAllEntry(self):
        return {
            "name": self.nameEntry.get(),
            "nextEpisode": self.nextEpisodeEntry.get(),
            "nextDate": self.nextReleaseDateEntry.get(),
            "time": self.timeEntry.get()
        }

    def isAllEntryValid(self):
        if not self.nameEntry.get():
            return False
        elif not self.nextEpisodeEntry.get():
            return False
        elif not self.nextReleaseDateEntry.get():
            return False
        elif not self.timeEntry.get():
            return False
        elif not self.nextEpisodeEntry.IsValid():
            return False
        elif not self.nextReleaseDateEntry.IsValid():
            return False
        elif not self.timeEntry.IsValid():
            return False
        return True

    def InitBasicWindow(self):
        self.ShowButtlerMessageBox()
        self.ShowShowRegisterWindowButton()

    def InitRegisterWindow(self):
        self.testRegisterMessage = tk.Message(self.registerFrame, text="登録画面は未実装")
        self.testRegisterMessage.grid(row=0, column=0, columnspan=2)

        self.nameEntryLabel = tk.Label(self.registerFrame, text="名前")
        self.nameEntryLabel.grid(row=1, column=0)
        self.nameEntry = tk.Entry(self.registerFrame, width=32)
        self.nameEntry.grid(row=1, column=1)

        self.nextEpisodeEntryLabel = tk.Label(self.registerFrame, text="次回放送の話数")
        self.nextEpisodeEntryLabel.grid(row=2, column=0)
        self.nextEpisodeEntry = CommonView.NumberEntry(self.registerFrame, (2, 1))

        self.nextReleaseDateLabel = tk.Label(self.registerFrame, text="次回放送日")
        self.nextReleaseDateLabel.grid(row=3, column=0)
        self.nextReleaseDateEntry = CommonView.DateEntry(self.registerFrame, (3, 1))

        self.timeLabel = tk.Label(self.registerFrame, text="放送時間")
        self.timeLabel.grid(row=4, column=0)
        self.timeEntry = CommonView.TimeEntry(self.registerFrame, (4, 1))

        self.registerButtonInRegisterWindow = tk.Button(self.registerFrame, text="登録", command=self.OnRegisterButtonClick)
        self.registerButtonInRegisterWindow.grid(row=5, column=1)

        self.returnToBasicFrameButton = tk.Button(self.registerFrame, text="戻る", command=self.ShowBasicWindow)
        self.returnToBasicFrameButton.grid(row=5, column=2)

        self.registerFailLabel = tk.Label(self.registerFrame, text="適切に各項目を入力してください", state="disabled")
        self.registerFailLabel.grid(row=6, column=0, columnspan=3)

    def ShowBasicWindow(self):
        self.basicFrame.tkraise()

    def ShowRegisterWindow(self):
        self.registerFrame.tkraise()

    def DrawButler(self):
        print("drawButlerは未実装")
        #self.canvas = tk.Canvas(self.window, width=320, height=320, bd=0, )

    def ShowShowRegisterWindowButton(self):
        registerButton = tk.Button(self.basicFrame, text="登録", command=self.OnShowRegisterWindowButtonClick)
        registerButton.grid(row=0, column=2)

    def ShowButtlerMessageBox(self):
        self.butlerMessage = tk.StringVar()
        self.butlerMessageBox = tk.Message(self.basicFrame, textvariable=self.butlerMessage)
        self.butlerMessageBox.grid(row=1, column=0, columnspan=2)

    def ShowMessageOneByOne(self, message, cancel, startCount=0, hasSetOnCancel=False):
        if cancel.canceled == True:
            return

        if not hasSetOnCancel:
           cancel.setOnCancel(self.SetMessageComplete, message)

        if len(message.message) <= startCount:
            self.SetMessageComplete(message)
            return

        self.ShowText(message.message[:startCount+1])

        afterId = self.window.after(int(message.period*1000), self.ShowMessageOneByOne, message, cancel, startCount+1)
        cancel.setId(self.window, afterId)

    def SetMessageComplete(self, message):
        self.ShowText(message.message)

    def ShowText(self, text):
        self.butlerMessage.set(text)

    def ShowRegisterFailLabel(self, isFail):
        if isFail:
            self.registerFailLabel.config(state="normal")
        else:
            self.registerFailLabel.config(state="disabled")
        self.registerFailLabel.update_idletasks()




    def OnRegisterButtonClick(self):
        for callback in self.onRegisterButtonClickCallback:
            callback()

    def OnShowRegisterWindowButtonClick(self):
        for callback in self.onShowRegisterWindowButtonClickCallback:
            callback()