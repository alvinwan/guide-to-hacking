import sys
import webview
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QEvent
import webview.platforms.qt  # needed for us to define a custom application


class MyApp(QApplication):
    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ApplicationActivate:
            window.set_title("In focus")
        if event.type() == QEvent.Type.ApplicationDeactivate:
            window.set_title("Not in focus")
        return super(QApplication, self).event(event)


if __name__ == '__main__':
    app = MyApp(sys.argv)
    window = webview.create_window('Hello world', 'https://alvinwan.com/blog/')
    webview.start(gui='qt')