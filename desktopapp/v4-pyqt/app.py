from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import QEvent


class MyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.window = QMainWindow()
        self.window.show()

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ApplicationActivate:
            self.window.setWindowTitle("In focus")
        if event.type() == QEvent.Type.ApplicationDeactivate:
            self.window.setWindowTitle("Not in focus")
        return super().event(event)


if __name__ == '__main__':
    app = MyApp([])
    app.exec()