import functools
import sys
from queue import Queue
from typing import Callable, TypeVar

from PySide2.QtCore import QMetaObject, QObject, Qt, Slot
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QLayout

app = None
tray_icon = None

T = TypeVar("T")


def create_qt_application() -> QApplication:
    global app

    if not app:
        app = QApplication(sys.argv)

    return app


def create_qt_tray_icon() -> QSystemTrayIcon:
    global tray_icon

    if not tray_icon:
        tray_icon = QSystemTrayIcon()

    return tray_icon


class Invoker(QObject):
    def __init__(self):
        super(Invoker, self).__init__()
        self.queue = Queue()

    def invoke(self, func, *args, **kw):
        self.queue.put(lambda: func(*args, **kw))
        QMetaObject.invokeMethod(self, "handler", Qt.QueuedConnection)

    @Slot()
    def handler(self):
        f = self.queue.get()
        f()


invoker = Invoker()


def ui_thread_call(f: Callable[..., T], *args, **kw) -> None:
    """
    Will call the given function on the PySide UI Thread. This means
    the function call is just queued, not invoked sync.
    """
    invoker.invoke(f, *args, **kw)


def ui_thread(f: Callable[..., T]) -> Callable[..., T]:
    """
    Ensures the call will happen on a UI thread. That means the call
    is just being queued, not invoked immediately.
    :param f:
    :return:
    """

    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        return invoker.invoke(f, *args, **kw)

    return wrapper


def show_notification(title: str, message: str, icon: QIcon, delay: int = 4000) -> None:
    """
    Shows a notification on the systray.
    :param title:
    :param message:
    :param icon:
    :param delay:
    :return:
    """
    global tray_icon
    assert tray_icon
    tray_icon.showMessage(title, message, icon, delay)


def clear_layout(layout: QLayout) -> None:
    while True:
        layout_item = layout.takeAt(0)
        if not layout_item:
            break

        layout_item.widget().deleteLater()


def _(callable: Callable[..., T]) -> Callable[[], T]:
    """
    Make a new callable that ignores all its parameters, and just calls the
    given callable.
    :param callable:
    :return:
    """

    def ignore_args(*args, **kw):
        return callable()

    return ignore_args
