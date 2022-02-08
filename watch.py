import threading
import time


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(
                self.next_call - time.time(), self._run)
            self._timer.daemon = True
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class Watchdog:
    checker = None
    callback = None
    course_number = None
    interval = None
    timer = None

    def __init__(self, course_number, checker, callback, interval=15):
        self.checker = checker
        self.callback = callback
        self.course_number = course_number
        self.interval = interval

    def check(self):
        from chiz import CourseManager, SessionManager
        import config
        course_manager = CourseManager(
            session_manager=SessionManager(
                username=config.username,
                password=config.password,
                base_url=config.base_url,
                login_path=config.login_path,
                check_path=config.check_path,
            ),
            course_base_path=config.course_base_path,
            ajax_path=config.ajax_path,
            view_path=config.view_path,
        )
        meeting_info = course_manager.get_meeting_info(self.course_number)
        join_url = course_manager.get_join_url(self.course_number)
        if self.checker(meeting_info):
            self.callback(meeting_info, self.timer, join_url)

    def start(self):
        self.timer = RepeatedTimer(self.interval, self.check)
        return self.timer
