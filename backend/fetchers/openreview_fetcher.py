"""Fetch conference papers from OpenReview API (ICLR, NeurIPS, ICML)."""

import openreview
from backend.models import Paper
from backend.processors.keyword_matcher import match_keywords


# OpenReview venue IDs for AI三大会
OPENREVIEW_VENUES = {
    "iclr_2026":    {"venue_id": "ICLR.cc/2026/Conference",    "name": "ICLR 2026"},
    "iclr_2025":    {"venue_id": "ICLR.cc/2025/Conference",    "name": "ICLR 2025"},
    "neurips_2025": {"venue_id": "NeurIPS.cc/2025/Conference",  "name": "NeurIPS 2025"},
    "neurips_2024": {"venue_id": "NeurIPS.cc/2024/Conference",  "name": "NeurIPS 2024"},
    "icml_2025":    {"venue_id": "ICML.cc/2025/Conference",     "name": "ICML 2025"},
    "icml_2024":    {"venue_id": "ICML.cc/2024/Conference",     "name": "ICML 2024"},
}

OPENREVIEW_BASE = "https://openreview.net"


def fetch_openreview_papers(conf_id: str, keyword_filter: bool = True) -> list:
    """Fetch accepted papers from OpenReview for a given conference.

    Args:
        conf_id: Conference ID (e.g., 'iclr_2026')
        keyword_filter: If True, only return papers matching keywords.
                        If False, return all accepted papers.
    """
    if conf_id not in OPENREVIEW_VENUES:
        raise ValueError(
            f"Unknown conference: {conf_id}. "
            f"Available: {', '.join(OPENREVIEW_VENUES.keys())}"
        )

    venue_info = OPENREVIEW_VENUES[conf_id]
    venue_id = venue_info["venue_id"]
    conf_name = venue_info["name"]

    print(f"  Connecting to OpenReview API...")
    client = openreview.api.OpenReviewClient(
        baseurl="https://api2.openreview.net"
    )

    # Get venue group to find submission invitation name
    venue_group = client.get_group(venue_id)
    submission_name = venue_group.content.get(
        "submission_name", {}
    ).get("value", "Submission")

    print(f"  Fetching accepted papers for {conf_name}...")
    notes = client.get_all_notes(
        invitation=f"{venue_id}/-/{submission_name}",
        content={"venueid": venue_id},
    )
    print(f"  Found {len(notes)} accepted papers")

    papers = []
    for note in notes:
        content = note.content or {}
        title = content.get("title", {}).get("value", "")
        abstract = content.get("abstract", {}).get("value", "")

        if not title:
            continue

        # Keyword matching
        tags = match_keywords(title, abstract)
        if keyword_filter and not tags:
            continue

        # Extract authors
        authors = content.get("authors", {}).get("value", [])

        # Build PDF URL
        pdf_path = content.get("pdf", {}).get("value", "")
        pdf_url = f"{OPENREVIEW_BASE}{pdf_path}" if pdf_path else ""

        # OpenReview forum URL
        forum_url = f"{OPENREVIEW_BASE}/forum?id={note.forum}"

        # Keywords from OpenReview
        or_keywords = content.get("keywords", {}).get("value", [])

        paper = Paper(
            arxiv_id=note.id,  # Use OpenReview ID
            title=title,
            authors=authors,
            abstract=abstract,
            arxiv_url=forum_url,
            pdf_url=pdf_url,
            primary_category=", ".join(or_keywords[:3]) if or_keywords else "",
            categories=or_keywords,
            tags=sorted(tags) if tags else [],
            published_date=conf_name,
            source="conference",
            conference=conf_name,
        )
        papers.append(paper)

    print(f"  Matched {len(papers)} papers (keyword_filter={keyword_filter})")
    return papers
