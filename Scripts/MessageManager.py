from Message import Message
import RoopCancel

class MessageManager:
    def __init__(self, window, saveData):
        self.window = window
        self.messageQueue = []
        self.cancellation = RoopCancel.RoopCancel()
        self.saveData = saveData

    def EnqueueMessage(self, message):
        self.messageQueue.append(message)
        if len(self.messageQueue) == 1:
            self.StartMessage()


    def StartMessage(self):
        message = self.messageQueue[0]
        self.window.ShowMessageOneByOne(message, self.cancellation)
        message.ShowButtons(self.window.buttonLeftText, self.window.buttonRightText)
        self.window.ActivateLeftRightButtons(True)
        self.window.onButtonRightClickCallback.append((self.OnButtonRightClicked,))
        self.window.onButtonLeftClickCallback.append((self.OnButtonLeftClicked,))

    def StartNextMessage(self):
        self.messageQueue.pop(0)
        self.cancellation.cancel()
        self.cancellation = RoopCancel.RoopCancel()

        if not self.messageQueue:
            self.ClearMessages()
        else:
            self.window.onButtonRightClickCallback.clear()
            self.window.onButtonLeftClickCallback.clear()
            self.window.ActivateLeftRightButtons(False)
            self.StartMessage()

    def OnButtonRightClicked(self):
        if not self.messageQueue:
            return

        if self.cancellation.canceled or self.messageQueue[0].isCompleted == True:
            self.messageQueue[0].OnButtonRightClick(self.saveData)
            self.StartNextMessage()
        else:
            self.cancellation.cancel()

    def OnButtonLeftClicked(self):
        if not self.messageQueue:
            return

        if self.cancellation.canceled or self.messageQueue[0].isCompleted == True:
            self.messageQueue[0].OnButtonLeftClick(self.saveData)
            self.StartNextMessage()
        else:
            self.cancellation.cancel()

    def ClearMessages(self):
        self.window.SetMessageComplete(Message.Message(""))
        self.window.ActivateLeftRightButtons(False)
        self.window.buttonLeftText.set("")
        self.window.buttonRightText.set("")
