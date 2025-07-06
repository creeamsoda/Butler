class RoopCancel:
    def __init__(self):
        self.canceled = False
        self.id = None
        self.onCancelCallback = []

    def setId(self, widget, afterId):
        self.widget = widget
        self.id = afterId

    def setOnCancel(self, function, *args):
        self.onCancelCallback.append((function, args))

    def cancel(self):
        self.canceled = True
        if self.id != None:
            print("after_cancel()")
            self.widget.after_cancel(self.id)
        for (function, args) in self.onCancelCallback:
            function(*args)
        return True