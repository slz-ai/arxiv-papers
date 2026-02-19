from typing import List, Optional

from pydantic import BaseModel


class Paper(BaseModel):
    arxiv_id: str
    title: str
    authors: List[str]
    abstract: str
    arxiv_url: str
    pdf_url: str
    primary_category: str
    categories: List[str]
    tags: List[str]
    published_date: str
    source: str  # "arxiv" or "conference"
    conference: Optional[str] = None


class DailyData(BaseModel):
    date: str
    paper_count: int
    papers: List[Paper]
    available_tags: List[str]


class ConferenceData(BaseModel):
    conference: str
    conference_id: str
    paper_count: int
    papers: List[Paper]
    available_tags: List[str]


class IndexData(BaseModel):
    last_updated: str
    available_dates: List[str]
    available_conferences: List[dict]
    all_tags: List[str]
