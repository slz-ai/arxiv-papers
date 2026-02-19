import arxiv
from datetime import date

from backend.config import ARXIV_CATEGORIES, ARXIV_MAX_RESULTS, ARXIV_DELAY_SECONDS
from backend.models import Paper
from backend.processors.keyword_matcher import match_keywords


def fetch_daily_papers(target_date: date) -> list[Paper]:
    """Fetch arXiv papers for a given date, filtered by keywords."""
    client = arxiv.Client(
        page_size=100,
        delay_seconds=ARXIV_DELAY_SECONDS,
        num_retries=3,
    )

    # Build category query
    cat_query = " OR ".join(f"cat:{c}" for c in ARXIV_CATEGORIES)

    # Date range for the target date
    date_start = target_date.strftime("%Y%m%d") + "0000"
    date_end = target_date.strftime("%Y%m%d") + "2359"
    query = f"({cat_query}) AND submittedDate:[{date_start} TO {date_end}]"

    search = arxiv.Search(
        query=query,
        max_results=ARXIV_MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    matched_papers = []
    for result in client.results(search):
        tags = match_keywords(result.title, result.summary)
        if not tags:
            continue

        arxiv_id = result.entry_id.split("/abs/")[-1]
        paper = Paper(
            arxiv_id=arxiv_id,
            title=result.title.strip().replace("\n", " "),
            authors=[a.name for a in result.authors],
            abstract=result.summary.strip().replace("\n", " "),
            arxiv_url=result.entry_id,
            pdf_url=result.pdf_url or f"https://arxiv.org/pdf/{arxiv_id}",
            primary_category=result.primary_category,
            categories=[c.term if hasattr(c, "term") else str(c) for c in result.categories],
            tags=sorted(tags),
            published_date=target_date.isoformat(),
            source="arxiv",
        )
        matched_papers.append(paper)

    return matched_papers
