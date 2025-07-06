from Message import Message

class AskYesNoMessage(Message.Message):
    def __init__(self, message, period=0.05):
        super().__init__(message, period)
