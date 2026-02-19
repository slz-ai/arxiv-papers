import json
from datetime import datetime

from backend.config import DAILY_DIR, CONFERENCE_DIR, INDEX_FILE, ALL_TAGS, CONFERENCES
from backend.models import Paper, DailyData, ConferenceData, IndexData

# All known conferences from both OpenReview and Semantic Scholar
def _get_all_conf_names():
    """Build a mapping of conf_id -> name from all known sources."""
    from backend.fetchers.openreview_fetcher import OPENREVIEW_VENUES
    from backend.fetchers.conference_fetcher import S2_VENUES
    names = {}
    for cid, v in OPENREVIEW_VENUES.items():
        names[cid] = v["name"]
    for cid, v in S2_VENUES.items():
        names[cid] = v["name"]
    for cid, v in CONFERENCES.items():
        names.setdefault(cid, v["name"])
    return names


def save_daily_papers(date_str: str, papers: list[Paper]) -> None:
    """Save daily papers to data/daily/{date}.json."""
    DAILY_DIR.mkdir(parents=True, exist_ok=True)

    all_tags = sorted(set(tag for p in papers for tag in p.tags))
    data = DailyData(
        date=date_str,
        paper_count=len(papers),
        papers=papers,
        available_tags=all_tags,
    )

    filepath = DAILY_DIR / f"{date_str}.json"
    filepath.write_text(json.dumps(data.model_dump(), indent=2, ensure_ascii=False))
    print(f"Saved {len(papers)} papers to {filepath}")


def save_conference_papers(conf_id: str, papers: list[Paper]) -> None:
    """Save conference papers to data/conferences/{conf_id}.json."""
    CONFERENCE_DIR.mkdir(parents=True, exist_ok=True)

    all_conf_names = _get_all_conf_names()
    conf_name = all_conf_names.get(conf_id, conf_id)
    all_tags = sorted(set(tag for p in papers for tag in p.tags))
    data = ConferenceData(
        conference=conf_name,
        conference_id=conf_id,
        paper_count=len(papers),
        papers=papers,
        available_tags=all_tags,
    )

    filepath = CONFERENCE_DIR / f"{conf_id}.json"
    filepath.write_text(json.dumps(data.model_dump(), indent=2, ensure_ascii=False))
    print(f"Saved {len(papers)} conference papers to {filepath}")


def update_index() -> None:
    """Rebuild data/index.json from existing data files."""
    # Collect available dates
    available_dates = sorted(
        [f.stem for f in DAILY_DIR.glob("*.json")],
        reverse=True,
    )

    # Collect available conferences - scan actual files, not just config dict
    all_conf_names = _get_all_conf_names()
    available_conferences = []
    for filepath in sorted(CONFERENCE_DIR.glob("*.json")):
        conf_id = filepath.stem
        name = all_conf_names.get(conf_id)
        if not name:
            # Read name from the file itself as fallback
            try:
                data = json.loads(filepath.read_text())
                name = data.get("conference", conf_id)
            except Exception:
                name = conf_id
        available_conferences.append({"id": conf_id, "name": name})

    index = IndexData(
        last_updated=datetime.utcnow().isoformat() + "Z",
        available_dates=available_dates,
        available_conferences=available_conferences,
        all_tags=ALL_TAGS,
    )

    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index.model_dump(), indent=2, ensure_ascii=False))
    print(f"Updated index: {len(available_dates)} dates, {len(available_conferences)} conferences")
