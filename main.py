#!/usr/bin/env python
import os
import yaml
from pathlib import Path
from scraper.client import JiraClient
from scraper.extractor import extract_all_projects
from transformer.writer import write_jsonl
from utils.logger import get_logger

log = get_logger("main")

def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    cfg = load_config()

    client = JiraClient(
        base_url=cfg["jira_base_url"],
        rps=cfg["requests_per_second"],
        timeout=cfg["timeout_seconds"],
        max_retries=cfg["max_retries"],
    )

    checkpoint_dir = Path(cfg["checkpoint_dir"])
    issues_iter = extract_all_projects(cfg["projects"], client, checkpoint_dir)

    out_path = Path(cfg["output_dir"]) / cfg["output_file"]
    write_jsonl(issues_iter, out_path, cfg["llm"])

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("❌ Please set OPENAI_API_KEY before running.")
    main()
