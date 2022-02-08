import warnings
from watch import Watchdog
from config import action_beep_check_all
from utils import beep

warnings.filterwarnings("ignore")

course_numbers = action_beep_check_all["course_numbers"]


def check(info):
    return info["info"]["returncode"] == "SUCCESS"


def callback(info, timer, join_url):
    beep()
    name = info["info"]["meetingName"]
    print(f"Join URL for course {name}:")
    print(join_url)
    timer.stop()


watchdogs = []

for num in course_numbers:
    print(f"\rAdding #{num} to watchlist...", end="")
    watchdog = Watchdog(
        course_number=num,
        checker=check,
        callback=callback,
        interval=30
    )
    watchdog.start()
    watchdogs.append(watchdog)

print("\rAdded",
      ", ".join(map(str, course_numbers)),
      "to watchlist successfully.")

while True:
    try:
        pass
    except KeyboardInterrupt:
        break
