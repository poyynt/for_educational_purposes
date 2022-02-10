import warnings
import sys
import threading
from watch import Watchdog
from utils import beep

warnings.filterwarnings("ignore")


def check(info):
    return info["info"]["returncode"] == "SUCCESS"


def callback(info, timer, join_url):
    timer.stop()
    beep()
    print("Join URL:")
    print(join_url)
    sys.exit(0)


Watchdog(
    course_number=input("course number: "),
    checker=check,
    callback=callback,
    interval=30
).start()

while threading.active_count() > 1:
    try:
        pass
    except KeyboardInterrupt:
        break
