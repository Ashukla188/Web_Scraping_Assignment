from pydantic import BaseModel, Field
from typing import List, Optional

class CommentAuthor(BaseModel):
    displayName: str

class Comment(BaseModel):
    id: str
    author: CommentAuthor
    body: str
    created: str

class IssueFields(BaseModel):
    summary: str
    description: Optional[str] = None
    status: dict
    priority: Optional[dict] = None
    assignee: Optional[dict] = None
    reporter: dict
    labels: List[str] = Field(default_factory=list)
    created: str
    updated: str
    comment: List[Comment] = Field(default_factory=list, alias="comments")

class RawIssue(BaseModel):
    key: str
    fields: IssueFields
