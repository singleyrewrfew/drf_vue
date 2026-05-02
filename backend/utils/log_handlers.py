import os
import logging.handlers


class SafeRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """
    Windows 兼容的日志轮转 Handler

    Django runserver 的 auto-reloader 会启动两个进程，
    两个进程都持有同一个日志文件的句柄。
    当日志文件达到 maxBytes 需要轮转时，os.rename() 在 Windows 上
    会因文件被占用而抛出 PermissionError。

    此 Handler 在轮转失败时静默跳过，仅保留一条警告，
    避免日志系统自身报错影响业务。
    """

    def doRollover(self):
        try:
            super().doRollover()
        except PermissionError:
            pass
