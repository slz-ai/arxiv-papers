"""Backfill past N days of arXiv papers."""

import sys
from datetime import date, timedelta

from backend.fetch_daily import main as fetch_daily


def backfill(days=7):
    today = date.today()
    for i in range(1, days + 1):
        target = today - timedelta(days=i)
        # Skip weekends (no arXiv announcements on Sat/Sun)
        if target.weekday() in (5, 6):
            print(f"Skipping {target.isoformat()} (weekend)")
            continue
        try:
            fetch_daily(target)
        except Exception as e:
            print(f"Error fetching {target.isoformat()}: {e}")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    backfill(n)
