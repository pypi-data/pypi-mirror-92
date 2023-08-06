import os
import abc

if os.name == 'nt':
    import win32con, win32file, pywintypes

    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0  # The default value
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    _overlapped = pywintypes.OVERLAPPED()  # noqa
else:
    import fcntl


class BaseLock(metaclass=abc.ABCMeta):
    def __init__(self, lock_file_path: str):
        self.f = open(lock_file_path, 'a')

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplemented

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplemented


class WindwosFileLock(BaseLock):
    def __enter__(self):
        hfile = win32file._get_osfhandle(self.f.fileno())
        win32file.LockFileEx(hfile, LOCK_EX, 0, 0xffff0000, _overlapped)

    def __exit__(self, exc_type, exc_val, exc_tb):
        hfile = win32file._get_osfhandle(self.f.fileno())
        win32file.UnlockFileEx(hfile, 0, 0xffff0000, _overlapped)


class LinuxFileLock(BaseLock):
    def __enter__(self):
        fcntl.flock(self.f, fcntl.LOCK_EX)

    def __exit__(self, exc_type, exc_val, exc_tb):
        fcntl.flock(self.f, fcntl.LOCK_UN)


FileLock = WindwosFileLock if os.name == 'nt' else LinuxFileLock

if __name__ == '__main__':
    """ 把这个脚本连续反复启动多个可以测试文件锁，只有获得文件锁，代码块才能执行"""
    import nb_log
    import time

    print('等待获得锁')
    with FileLock('testx.lock'):
        print('hi')
        time.sleep(20)
        print('hello')
