from Message import AskYesNoMessage

class AskWatchedMessage(AskYesNoMessage.AskYesNoMessage):
	def __init__(self, message, period=0.05):
		super().__init__(message, period)

	yesText = {"はい"}
	noText = {"いいえ"}