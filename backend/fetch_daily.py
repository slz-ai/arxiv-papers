"""Fetch daily arXiv papers and save to data/daily/{date}.json."""

import sys
from datetime import date, timedelta

from backend.fetchers.arxiv_fetcher import fetch_daily_papers
from backend.storage import save_daily_papers, update_index


def main(target_date=None) -> None:
    if target_date is None:
        # Default: fetch yesterday's papers (arXiv announces previous day's submissions)
        target_date = date.today() - timedelta(days=1)

    print(f"Fetching arXiv papers for {target_date.isoformat()}...")
    papers = fetch_daily_papers(target_date)
    print(f"Found {len(papers)} matching papers")

    save_daily_papers(target_date.isoformat(), papers)
    update_index()


if __name__ == "__main__":
    target = None
    if len(sys.argv) > 1:
        target = date.fromisoformat(sys.argv[1])
    main(target)
