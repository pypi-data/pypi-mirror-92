import requests
from selenium.webdriver.chrome.options import Options
from umdriver import UMDriver


def parse_hostname(hostname: str) -> str:
    if hostname.lower().startswith("http"):
        return hostname.rstrip("/")
    return f"https://{hostname}".rstrip("/")


class SlateSession:
    def __init__(
        self, hostname: str, username: str, password: str, external: bool = False
    ):
        self.hostname = parse_hostname(hostname)
        self.username = username
        self.password = password
        self.external = external
        self._session = None

    def __getattr__(self, item):
        """Host attributes from self.session to top-level so class functions like a requests.Session object."""
        return getattr(self.session, item)

    @property
    def session(self) -> requests.Session:
        """
        Returns an authenticated session object.
        """
        if self._session is None:
            self._session = self.get_session()
        return self._session

    def get_session(self) -> requests.Session:
        """
        Generic function that returns an authenticated session object.
        """
        if self.external:
            return self.get_external_session()
        return self.get_internal_session()

    def get_external_session(self) -> requests.Session:
        """
        Authenticate as an external user and returns a session object.
        """
        url = f"{self.hostname}/manage/login?cmd=external"
        session = requests.session()
        session.headers.update({"Origin": self.hostname})
        r1 = session.get(url)
        r2 = session.post(
            r1.url, data={"user": self.username, "password": self.password}
        )
        r2.raise_for_status()
        return session

    def get_internal_session(self) -> requests.Session:
        """
        Authenticates as an internal user and returns a session object.

        Authentication is done via headless Chrome (Selenium) before passing the session tokens to the returned
        session object.
        """
        opts = Options()
        opts.headless = True
        session = requests.session()
        with UMDriver(options=opts) as d:
            d.login(self.username, self.password)
            d.get(f"{self.hostname}/manage")
            for c in d.get_cookies():
                session.cookies.set(c["name"], c["value"])
        headers = {
            "Host": self.hostname.replace("https://", ""),
            "Origin": self.hostname,
        }
        session.headers.update(headers)
        return session
