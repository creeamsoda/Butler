from Message import AskYesNoMessage
import random

class AskWatchedMessage(AskYesNoMessage.AskYesNoMessage):
	def __init__(self, anime, period=0.05):
		self.name = anime["name"]
		print(anime)
		super().__init__(self.CreateMessage(anime), period)

	yesText = {"はい"}
	noText = {"いいえ"}
	
	def ShowButtons(self, buttonLeftTextVar, buttonRightTextVar):
		randomYesIndex = random.randrange(len(self.yesText))
		randomNoIndex = random.randrange(len(self.noText))
		buttonRightTextVar.set(list(self.yesText)[randomYesIndex])
		buttonLeftTextVar.set(list(self.noText)[randomNoIndex])

	def OnButtonLeftClick(self, saveData):
		return None

	def OnButtonRightClick(self, saveData):
		saveData.SetWatched(self.name)

	def CreateMessage(self, anime):
		#FIXME:今週か先週かの判定を追加する
		return f"前回の{anime["name"]}はご覧になりましたか？"