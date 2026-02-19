"""Fetch conference papers from Semantic Scholar API (NLP三大会)."""

import os
import time

import httpx

from backend.models import Paper
from backend.processors.keyword_matcher import match_keywords

S2_BASE = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "externalIds,title,abstract,authors,venue,year,publicationDate,url,openAccessPdf"

# Full venue names as indexed in Semantic Scholar
S2_VENUES = {
    "acl_2025":   {"name": "ACL 2025",   "venue": "Annual Meeting of the Association for Computational Linguistics", "year": "2025"},
    "acl_2024":   {"name": "ACL 2024",   "venue": "Annual Meeting of the Association for Computational Linguistics", "year": "2024"},
    "emnlp_2025": {"name": "EMNLP 2025", "venue": "Conference on Empirical Methods in Natural Language Processing",  "year": "2025"},
    "emnlp_2024": {"name": "EMNLP 2024", "venue": "Conference on Empirical Methods in Natural Language Processing",  "year": "2024"},
    "naacl_2025": {"name": "NAACL 2025", "venue": "North American Chapter of the Association for Computational Linguistics", "year": "2025"},
    "naacl_2024": {"name": "NAACL 2024", "venue": "North American Chapter of the Association for Computational Linguistics", "year": "2024"},
}


def fetch_conference_papers(conf_id: str) -> list:
    """Fetch papers for a NLP conference using Semantic Scholar bulk search API."""
    if conf_id not in S2_VENUES:
        raise ValueError(
            f"Unknown S2 conference: {conf_id}. "
            f"Available: {', '.join(S2_VENUES.keys())}"
        )

    conf = S2_VENUES[conf_id]
    api_key = os.environ.get("S2_API_KEY")

    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    papers = []
    token = None

    print(f"  Using Semantic Scholar bulk API for {conf['name']}...")

    while True:
        params = {
            "query": "*",
            "venue": conf["venue"],
            "year": conf["year"],
            "fields": S2_FIELDS,
            "limit": 100,
        }
        if token:
            params["token"] = token

        resp = httpx.get(
            f"{S2_BASE}/paper/search/bulk",
            params=params,
            headers=headers,
            timeout=30.0,
        )

        if resp.status_code == 429:
            print("  Rate limited, waiting 30s...")
            time.sleep(30)
            continue

        resp.raise_for_status()
        data = resp.json()

        for p in data.get("data", []):
            if not p.get("title") or not p.get("abstract"):
                continue

            tags = match_keywords(p["title"], p.get("abstract", ""))

            ext_ids = p.get("externalIds") or {}
            arxiv_id = ext_ids.get("ArXiv", "")
            arxiv_url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else (p.get("url") or "")
            pdf_url = ""
            if p.get("openAccessPdf"):
                pdf_url = p["openAccessPdf"].get("url", "")
            if not pdf_url and arxiv_id:
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

            authors = [a.get("name", "") for a in (p.get("authors") or [])]

            paper = Paper(
                arxiv_id=arxiv_id or p.get("paperId", ""),
                title=p["title"],
                authors=authors,
                abstract=p.get("abstract", ""),
                arxiv_url=arxiv_url,
                pdf_url=pdf_url,
                primary_category="",
                categories=[],
                tags=sorted(tags) if tags else [],
                published_date=p.get("publicationDate") or conf["year"],
                source="conference",
                conference=conf["name"],
            )
            papers.append(paper)

        token = data.get("token")
        fetched = len(data.get("data", []))
        print(f"  Fetched batch of {fetched}, total so far: {len(papers)}")

        if not token or fetched == 0:
            break

        time.sleep(1.0)

    print(f"  Done: {len(papers)} papers from {conf['name']}")
    return papers
