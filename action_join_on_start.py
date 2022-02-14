import warnings
from watch import Watchdog
from config import action_join_on_start
from utils import beep

warnings.filterwarnings("ignore")


def check(info):
    return info["info"]["returncode"] == "SUCCESS"


def callback(info, timer, join_url):
    try:
        timer.stop()
        beep()
        print("Join URL:")
        print(join_url)
        import time
        import random
        random_sleep = random.randint(*action_join_on_start["random_range"])
        print(f"Joining meeting automatically after {random_sleep}s.",
              f"t={time.time()}")
        time.sleep(random_sleep)
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
                    (By.CSS_SELECTOR, ".icon-bbb-group_chat")
                )
            )
            time.sleep(.5)
        print("Meeting has ended, enabling watchdog and quitting.",
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
