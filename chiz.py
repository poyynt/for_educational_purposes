class SessionManager:
    _username = None
    _password = None
    base_url = None
    login_path = None
    check_path = "my/"
    session = None
    _sesskey = None

    def __init__(self, username, password, base_url, login_path):
        self._username = username
        self._password = password
        self.base_url = base_url
        self.login_path = login_path
        import requests
        self.session = requests.Session()

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
        if self._is_logged_in():
            return self._sesskey

    def get(self, path, params=None):
        if not self._is_logged_in():
            self._login()
        return self.session.get(
            self.base_url + path, params=params, verify=False)


class CourseManager:
    session_manager = None
    course_base_path = None
    ajax_url = None

    def __init__(self, session_manager, course_base_path, ajax_url):
        self.session_manager = session_manager
        self.course_base_path = course_base_path
        self.ajax_url = ajax_url

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
            self.ajax_url, params={
                "sesskey": sesskey,
                "id": course_id,
                "action": "meeting_info",
                "bigbluebuttonbn": bn_id,
                "updatecache": "false",
                "callback": "a"
            })
        import json
        return json.loads(req.text[2:-2])
