from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QEvent


class MyApp(QApplication): # subclass application
    def event(self, event: QEvent): # custom event handler
        if event.type() == QEvent.Type.FileOpen: # handle "File Open" event
            print(event.url())  # log the deeplink to console
        return super().event(event)


if __name__ == "__main__":
    app = MyApp([])
    app.exec()