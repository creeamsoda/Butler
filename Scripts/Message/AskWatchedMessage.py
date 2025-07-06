from Message import AskYesNoMessage
import random

class AskWatchedMessage(AskYesNoMessage.AskYesNoMessage):
	def __init__(self, message, period=0.05):
		super().__init__(message, period)

	yesText = {"はい"}
	noText = {"いいえ"}
	
	def ShowButtons(self, buttonLeft, buttonRight, buttonLeftTextVar, buttonRightTextVar):
		randomYesIndex = random.randrange(range(len(self.yesText)))
		randomNoIndex = random.randrange(range(len(self.noText)))
		buttonLeftTextVar.set(list(self.yesText)[randomYesIndex])
		buttonRightTextVar.set(list(self.noText)[randomNoIndex])
		buttonLeft.configure(state="disabled")
		buttonRight.configure(state="disabled")

	def OnButtonClick(self):
		