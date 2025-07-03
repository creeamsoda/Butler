class RoopCancel:
    def __init__(self):
        self.canceled = False

    def setId(self, widget, afterId):
        self.widget = widget
        self.id = afterId

    def cancel(self):
        self.canceled = True
        if self.id is str:
            self.widget.after_cancel(self.id)
        return True