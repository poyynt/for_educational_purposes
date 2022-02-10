def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance


@singleton
class SessionManager:
    _username = None
    _password = None
    base_url = None
    login_path = None
    check_path = None
    session = None
    _sesskey = None

    def __init__(self, username, password, base_url, login_path, check_path):
        self._username = username
        self._password = password
        self.base_url = base_url
        self.login_path = login_path
        self.check_path = check_path
        import requests
        import os
        import pickle
        if os.path.exists(".chiz_session.pickle"):
            with open(".chiz_session.pickle", "rb") as f:
                self.session = pickle.load(f)
        else:
            self.session = requests.Session()

    def __del__(self):
        import pickle
        with open(".chiz_session.pickle", "wb") as f:
            pickle.dump(self.session, f)

    def _is_logged_in(self):
        req = self.session.get(self.base_url + self.check_path, verify=False)
        if req.url == self.base_url + self.check_path:
            return True
        return False

    def _login(self):
        if self._is_logged_in():
            return
        req = self.session.get(self.base_url + self.login_path, verify=False)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(req.text, "html.parser")
        token = soup.find("input", {"name": "logintoken"})["value"]
        req = self.session.post(self.base_url + self.login_path,
                                data={
                                    "logintoken": token,
                                    "username": self._username,
                                    "password": self._password
                                },
                                verify=False)
        assert self._is_logged_in()
        soup = BeautifulSoup(req.text, "html.parser")
        from utils import get_cfg_from_script
        config_script = soup.find_all("script")[1].contents[0]
        self._sesskey = get_cfg_from_script(config_script)["sesskey"]
        return

    def get_sesskey(self):
        if not self._is_logged_in():
            self._login()
        return self._sesskey

    def get(self, path, params=None):
        if not self._is_logged_in():
            self._login()
        return self.session.get(
            self.base_url + path, params=params, verify=False)

    def head(self, path, params=None):
        if not self._is_logged_in():
            self._login()
        return self.session.head(
            self.base_url + path, params=params, verify=False)


@singleton
class CourseManager:
    session_manager = None
    course_base_path = None
    ajax_path = None
    view_path = None

    def __init__(
            self, session_manager, course_base_path, ajax_path, view_path):
        self.session_manager = session_manager
        self.course_base_path = course_base_path
        self.ajax_path = ajax_path
        self.view_path = view_path

    def _get_course_id(self, course_number):
        req = self.session_manager.get(
            self.course_base_path, params={"id": course_number})
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(req.text, "html.parser")
        script = soup.find_all("script")[-1].contents[0]
        from utils import get_course_id_from_script
        return get_course_id_from_script(script)

    def _get_bn_id(self, course_number):
        req = self.session_manager.get(
            self.course_base_path, params={"id": course_number})
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(req.text, "html.parser")
        script = soup.find_all("script")[-1].contents[0]
        from utils import get_bn_id_from_script
        return get_bn_id_from_script(script)

    def get_meeting_info(self, course_number):
        course_id = self._get_course_id(course_number)
        bn_id = self._get_bn_id(course_number)
        sesskey = self.session_manager.get_sesskey()
        req = self.session_manager.get(
            self.ajax_path, params={
                "sesskey": sesskey,
                "id": course_id,
                "action": "meeting_info",
                "bigbluebuttonbn": bn_id,
                "updatecache": "false",
                "callback": "a"
            })
        import json
        return json.loads(req.text[2:-2])

    def get_join_url(self, course_number):
        meeting_info = self.get_meeting_info(course_number)
        raw_url = meeting_info["status"]["join_url"]
        from urllib.parse import urlsplit, parse_qsl
        splitted = urlsplit(raw_url)
        params = dict(parse_qsl(splitted.query))
        req = self.session_manager.head(self.view_path, params=params)
        return req.next.url
