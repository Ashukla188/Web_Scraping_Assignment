import json
from pathlib import Path
from typing import Iterable
from utils.logger import get_logger
from .cleaner import html_to_text
from .tasks import derive_tasks

log = get_logger(__name__)

def write_jsonl(issues: Iterable[dict], out_path: Path, llm_cfg: dict):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for issue in issues:
            fields = issue.get("fields", {})
            title = fields.get("summary", "")
            description = html_to_text(fields.get("description", ""))

            comments_raw = fields.get("comment", [])
            comments = [
                f"{c['author']['displayName']} ({c['created']}): {html_to_text(c['body'])}"
                for c in comments_raw
            ]

            full_text = f"Title: {title}\nDescription: {description}\nComments:\n" + "\n".join(comments)

            derived = derive_tasks(
                full_text,
                model=llm_cfg["model"],
                temperature=llm_cfg["temperature"],
                max_tokens=llm_cfg["max_tokens"],
            )

            record = {
                "issue_key": issue["key"],
                "project": issue["key"].split("-")[0],
                "title": title,
                "status": fields.get("status", {}).get("name"),
                "priority": fields.get("priority", {}).get("name") if fields.get("priority") else None,
                "reporter": fields.get("reporter", {}).get("displayName"),
                "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
                "labels": fields.get("labels", []),
                "created": fields.get("created"),
                "updated": fields.get("updated"),
                "description": description,
                "comments": comments,
                "derived": derived,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    log.info("✅ Wrote JSONL → %s", out_path)
