import threading
import time

import requests
from urllib3.exceptions import ReadTimeoutError

threadLock = threading.Lock()
threads = []


class BackgroundRun(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        # Get lock to synchronize threads
        threadLock.acquire()
        # print_time(self.name, self.counter, 3)
        # Free lock to release next thread
        threadLock.release()


class Service:
    @staticmethod
    def StartNewThread(target_method):
        t = threading.Thread(target=target_method)
        t.start()

    @staticmethod
    def LoopMem(total_members: int, block_count: int, callback):
        Service.LoopMemberGraceService(total_members, block_count, 5, False, callback)

    @staticmethod
    def LoopMemberGraceService(total_members: int, block_count: int, interval_time_sec: int, once: bool, callback=None):
        last = 1
        (loops, left) = divmod(total_members, block_count)
        while True:
            try:
                if loops > 0:
                    for x in range(loops):
                        a = x * block_count
                        b = a + block_count
                        if callback is not None:
                            callback(a, b)
                        last = b

                if left == 0 and once:
                    break

                if left > 0:
                    if callback is not None:
                        callback(last, left)

                time.sleep(interval_time_sec)

                if once:
                    break

            except TypeError as te:
                print("☯︎ some type errors", te)
                continue

            except requests.exceptions.Timeout as eg:
                # Maybe set up for a retry, or continue in a retry loop
                print("☯︎ request time out", eg)
                continue

            except requests.exceptions.ConnectionError as ef:
                # Maybe set up for a retry, or continue in a retry loop
                print("☯︎ request time out", ef)
                continue

            except ReadTimeoutError as h:
                print("☯︎ time out", h)
                continue

            except requests.exceptions.RequestException as ej:
                # catastrophic error. bail.
                print("☯︎ nothing but try again later", ej)
                continue
