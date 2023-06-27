import webview
import webview.platforms.qt
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QEvent


def event_handler(self, event: QEvent):
    if event.type() == QEvent.Type.ApplicationActivate:
        window.set_title("In focus")
    if event.type() == QEvent.Type.ApplicationDeactivate:
        window.set_title("Not in focus")
    return super(QApplication, self).event(event)
webview.platforms.qt.QApplication.event = event_handler  # HACK: monkey patch webview's qt event handler


if __name__ == '__main__':
    window = webview.create_window('Hello world', 'https://alvinwan.com/blog/')
    webview.start(gui='qt')