class Message:
    def __init__(self, message, period=0.05):
        self.message = message
        self.period = period
        self.isCompleted = False

    def ShowButtons(self, frame, gird):
        return None
