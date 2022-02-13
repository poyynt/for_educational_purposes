import warnings
from watch import Watchdog
from config import action_join_and_leave_with_user
from utils import beep

warnings.filterwarnings("ignore")


def check(info):
    if info["info"]["returncode"] != "SUCCESS":
        return False
    for attendee in info["info"]["attendees"]["attendee"]:
        if attendee["userID"] == action_join_and_leave_with_user["user_id"]:
            return True
    return False


def callback(info, timer, join_url):
    try:
        timer.stop()
        beep()
        print("Join URL:")
        print(join_url)
        import time
        print(f"Joining meeting automatically. t={time.time()}")
        target_user_name = None
        for attendee in info["info"]["attendees"]["attendee"]:
            if attendee["userID"] == \
                    action_join_and_leave_with_user["user_id"]:
                target_user_name = attendee["fullName"]
        if target_user_name is None:
            timer.start()
            print("ERROR: callback called but target user is not present.")
            return
        from selenium.webdriver import Firefox
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import TimeoutException
        firefox = Firefox()
        firefox.implicitly_wait(5)
        firefox.get(join_url)
        try:
            WebDriverWait(firefox, 30).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".icon-bbb-listen")
                )
            ).click()
        except TimeoutException:
            print("cannot join audio conference: element not found.")
        try:
            WebDriverWait(firefox, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".icon-bbb-thumbs_up")
                )
            ).click()
        except TimeoutException:
            pass
        firefox.implicitly_wait(5)
        for _ in range(16):
            WebDriverWait(firefox, 60 * 90).until_not(
                EC.presence_of_element_located(
                    (By.XPATH,
                     f"//*[text()='{target_user_name}']"
                     )
                )
            )
            time.sleep(.5)
        print("Target user has left, enabling watchdog and leaving.",
              f"t={time.time()}")
        firefox.quit()
    finally:
        timer.start()


Watchdog(
    course_number=input("course number: "),
    checker=check,
    callback=callback,
    interval=3
).start()

while True:
    try:
        pass
    except KeyboardInterrupt:
        break
