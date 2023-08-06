mopyx utilities when working with PySide2 (the official Qt5 python
bindings)

Installation
============

.. code:: sh

    pip install mopyx_pyside2

API
===

-  ``create_qt_application()`` → create a Qt5 application.

-  ``create_qt_tray_icon()`` → create a systray icon.

-  ``ui_thread_call(f, args, kw)`` → invoke a function on the Qt’s UI
   thread.

-  ``ui_thread(f)`` → make the function invokable on the Qt’s UI thread.

-  ``show_notification(title: str, message: str, icon: QIcon, delay: int = 4000)``
   → shows a notification on the systray.

-  ``clear_layout(layout: QLayout)`` → clear the layout.

-  ``_(f)`` → create a callable that ignores all its parameters, and
   invokes the callable given as an argument.

Sample
======

How to call functions from a different thread, still accessing the UI:

.. code:: python

    @ui_thread
    @action
    def update_failed_count(job, successful: bool) -> None:
        # ...

    @ui_thread
    @action
    def update_results(job, result) -> None:
        # ...

    class JobMonitorThread(threading.Thread):
        def run(self) -> None:
            try:
                # do something
            except Exception:
                update_failed_count(job, False)
            else:
                update_results(job, ...)

            time.sleep(10)
