from utils.checkpoint import Checkpoint
from utils.logger import get_logger
from .client import JiraClient
from .models import RawIssue
from typing import Iterator

log = get_logger(__name__)

def _build_jql(project: str) -> str:
    return f'project = "{project}" ORDER BY created ASC'

class JiraPaginator:
    """Iterates through Jira issues for a given project using pagination."""
    def __init__(self, client: JiraClient, project: str, checkpoint: Checkpoint):
        self.client = client
        self.project = project
        self.checkpoint = checkpoint
        self.jql = _build_jql(project)

    def __iter__(self) -> Iterator[RawIssue]:
        start_at = self.checkpoint.get(f"{self.project}_start", 0)
        batch = 100

        while True:
            data = self.client.search_issues(self.jql, start_at=start_at, max_results=batch)
            issues = [RawIssue(**i) for i in data.get("issues", [])]

            if not issues:
                break

            for issue in issues:
                full = self.client.get_issue(issue.key)
                issue.fields.comment = full["fields"].get("comment", {}).get("comments", [])
                yield issue

            start_at += len(issues)
            self.checkpoint.set(f"{self.project}_start", start_at)
            log.info("Fetched %s issues for %s (startAt=%s)", len(issues), self.project, start_at)

            if len(issues) < batch:
                break
