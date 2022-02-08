import warnings
from watch import Watchdog
from utils import beep

warnings.filterwarnings("ignore")


def check(info):
    return info["info"]["returncode"] == "SUCCESS"


def callback(info, timer, join_url):
    beep()
    print("Join URL:")
    print(join_url)
    timer.stop()


Watchdog(
    course_number=input("course number: "),
    checker=check,
    callback=callback,
    interval=30
).start()

while True:
    try:
        pass
    except KeyboardInterrupt:
        break
