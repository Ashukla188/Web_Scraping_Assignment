import time
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from utils.logger import get_logger

log = get_logger(__name__)

class JiraClient:
    """Handles low-level Jira REST requests with retry & rate-limit."""
    def __init__(self, base_url: str, rps: int, timeout: int, max_retries: int):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.rps = rps
        self.timeout = timeout
        self.max_retries = max_retries
        self._last_call = 0.0

    def _rate_limit(self):
        now = time.time()
        elapsed = now - self._last_call
        sleep_for = max(0, 1.0 / self.rps - elapsed)
        if sleep_for > 0:
            time.sleep(sleep_for)
        self._last_call = time.time()

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((requests.RequestException,)),
        reraise=True,
    )
    def _get(self, url: str, params: dict | None = None):
        self._rate_limit()
        resp = self.session.get(url, params=params, timeout=self.timeout)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 60))
            log.warning("Rate limited, sleeping %ss", retry_after)
            time.sleep(retry_after)
            raise requests.HTTPError("429 Too Many Requests")
        resp.raise_for_status()
        return resp.json()

    def search_issues(self, jql: str, start_at: int, max_results: int = 100):
        url = f"{self.base_url}/rest/api/2/search"
        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "fields": "*all",
            "expand": "renderedFields,comment"
        }
        return self._get(url, params)

    def get_issue(self, key: str):
        url = f"{self.base_url}/rest/api/2/issue/{key}"
        params = {"fields": "*all", "expand": "renderedFields,comment"}
        return self._get(url, params)
