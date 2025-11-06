import os
import json
from utils.logger import get_logger
from openai import OpenAI

log = get_logger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are an expert software engineer.
Given a Jira issue (title, description, comments), produce:
1. summary – one concise sentence
2. classification – one of: Bug, Feature, Improvement, Task, Other
3. qa – one high-quality Q&A pair from the issue discussion
Return ONLY valid JSON with keys: summary, classification, qa.
"""

def derive_tasks(issue_text: str, model: str, temperature: float, max_tokens: int) -> dict:
    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": issue_text},
            ],
        )
        raw = resp.choices[0].message.content.strip()
        return json.loads(raw)
    except Exception as e:
        log.error("LLM derive_tasks failed: %s", e)
        return {"summary": "", "classification": "Other", "qa": {"question": "", "answer": ""}}
