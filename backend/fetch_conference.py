"""Fetch conference papers and save to data/conferences/{conf_id}.json."""

import sys

from backend.config import CONFERENCES
from backend.fetchers.openreview_fetcher import OPENREVIEW_VENUES, fetch_openreview_papers
from backend.fetchers.conference_fetcher import S2_VENUES, fetch_conference_papers
from backend.storage import save_conference_papers, update_index


def main(conf_id=None):
    if conf_id is None:
        print("Available conferences:")
        print("\n  [OpenReview - no API key needed]")
        for cid in OPENREVIEW_VENUES:
            print(f"    {cid}: {OPENREVIEW_VENUES[cid]['name']}")
        print("\n  [Semantic Scholar - needs S2_API_KEY]")
        for cid, conf in CONFERENCES.items():
            if cid not in OPENREVIEW_VENUES:
                print(f"    {cid}: {conf['name']}")
        print("\nUsage: python -m backend.fetch_conference <conference_id>")
        print("  Or: python -m backend.fetch_conference all_openreview")
        return

    if conf_id == "all_openreview":
        conf_ids = list(OPENREVIEW_VENUES.keys())
    elif conf_id == "all_s2":
        conf_ids = list(S2_VENUES.keys())
    elif conf_id == "all":
        conf_ids = list(OPENREVIEW_VENUES.keys()) + list(S2_VENUES.keys())
    else:
        conf_ids = [conf_id]

    for cid in conf_ids:
        if cid in OPENREVIEW_VENUES:
            print(f"\nFetching {OPENREVIEW_VENUES[cid]['name']} from OpenReview...")
            papers = fetch_openreview_papers(cid)
            save_conference_papers_generic(cid, OPENREVIEW_VENUES[cid]["name"], papers)
        elif cid in S2_VENUES:
            print(f"\nFetching {S2_VENUES[cid]['name']} from Semantic Scholar...")
            papers = fetch_conference_papers(cid)
            save_conference_papers_generic(cid, S2_VENUES[cid]["name"], papers)
        else:
            print(f"Unknown conference: {cid}")
            continue

    update_index()


def save_conference_papers_generic(conf_id, conf_name, papers):
    """Save conference papers using the storage module."""
    from backend.config import CONFERENCES
    # Ensure the conference is in CONFERENCES for storage
    if conf_id not in CONFERENCES:
        CONFERENCES[conf_id] = {"name": conf_name, "venue": conf_name, "year": ""}
    save_conference_papers(conf_id, papers)


if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else None
    main(cid)
