from ctypes import windll


ES_SYSTEM_REQUIRED = 0x00000001
ES_CONTINUOUS = 0x80000000


def wek():
    windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
    windll.user32.MessageBoxA(0, b"Close this popup to allow your computer to sleep", b"Wek!", 0)
    windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)


if __name__ == '__main__':
    wek()