from pathlib import Path
from utils.checkpoint import Checkpoint
from utils.logger import get_logger
from .pagination import JiraPaginator
from typing import Iterable
from .client import JiraClient
from .models import RawIssue

log = get_logger(__name__)

def extract_all_projects(projects: list[str], client: JiraClient, checkpoint_dir: Path) -> Iterable[RawIssue]:
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    cp = Checkpoint(checkpoint_dir / "global.json")

    for proj in projects:
        proj_cp = Checkpoint(checkpoint_dir / f"{proj}.json")
        paginator = JiraPaginator(client, proj, proj_cp)

        for issue in paginator:
            yield issue.model_dump()

        cp.set(f"completed_{proj}", True)
        log.info("✅ Finished project %s", proj)
