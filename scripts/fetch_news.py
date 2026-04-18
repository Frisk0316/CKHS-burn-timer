#!/usr/bin/env python3
"""Daily news fetcher for the CKSH burn timer.

Searches Google News RSS for 建中-related controversy coverage,
updates incidents.json with new items, and auto-advances last_incident
when a high-confidence incident is detected.
"""

import json
import os
import sys
import re
import calendar
import urllib.parse
from datetime import datetime, timezone, timedelta

try:
    import feedparser
except ImportError:
    print("feedparser not installed. Run: pip install feedparser", file=sys.stderr)
    sys.exit(1)

# ── Configuration ─────────────────────────────────────────────────────────────

QUERIES = [
    "建國高中 炎上",
    "建中 炎上",
    "建中生 爭議",
    "建中 道歉",
    "建中 批評",
    "建中 privilege",
    "建中 特權",
    "建中 挨批",
    "建中 惹議",
    "建中 性平",
]

# Any match → add to recent_news
INCIDENT_RE = re.compile(
    r'炎上|道歉|撤下|撤展|抵制|批評|爭議|性平|歧視|privilege|特權|'
    r'網暴|公審|霸凌|挨批|惹議|挨轟|不雅|失言|歧視',
    re.IGNORECASE,
)

# High-confidence → also consider updating last_incident date
HIGH_CONF_RE = re.compile(
    r'炎上|道歉|撤下|撤展|網暴',
    re.IGNORECASE,
)

TW = timezone(timedelta(hours=8))
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'incidents.json')
MAX_AGE_DAYS = 60
RECENT_NEWS_CAP = 100

DOMAIN_LABELS = {
    'newtalk.tw': 'Newtalk',
    'ettoday.net': 'ETtoday',
    'ltn.com.tw': '自由時報',
    'udn.com': '聯合新聞網',
    'chinatimes.com': '中時',
    'cna.com.tw': '中央社',
    'ctwant.com': 'CTWANT',
    'nownews.com': 'NOWnews',
    'storm.mg': '風傳媒',
    'businesstoday.com.tw': '今周刊',
    'gvm.com.tw': '遠見雜誌',
    'setn.com': '三立新聞',
    'tvbs.com.tw': 'TVBS',
    'mirrormedia.mg': '鏡週刊',
    'dcard.tw': 'Dcard',
    'ptt.cc': 'PTT',
    'threads.com': 'Threads',
    'threads.net': 'Threads',
}


def source_label(url: str) -> str:
    for key, label in DOMAIN_LABELS.items():
        if key in url:
            return label
    try:
        parts = urllib.parse.urlparse(url).netloc.split('.')
        return '.'.join(parts[-2:]) if len(parts) >= 2 else url
    except Exception:
        return url


def fetch_feed(query: str) -> list:
    encoded = urllib.parse.quote(query)
    url = (
        f"https://news.google.com/rss/search"
        f"?q={encoded}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    )
    feed = feedparser.parse(url)
    return feed.entries or []


def parse_date(entry) -> tuple:
    """Return (datetime | None, 'YYYY-MM-DD')."""
    if entry.get('published_parsed'):
        ts = calendar.timegm(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(TW)
        return dt, dt.strftime('%Y-%m-%d')
    return None, datetime.now(TW).strftime('%Y-%m-%d')


def clean_title(title: str) -> str:
    # Google News appends "- Source Name" to titles; strip it
    return re.sub(r'\s*[-–—]\s*\S.*$', '', title).strip()


def main() -> None:
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Build deduplication set from existing data
    seen: set[str] = set()
    for item in data.get('recent_news', []):
        seen.add(item['url'])
    for inc in data.get('incidents', []):
        for src in inc.get('sources', []):
            seen.add(src['url'])

    cutoff = datetime.now(TW) - timedelta(days=MAX_AGE_DAYS)
    new_items: list[dict] = []

    for query in QUERIES:
        try:
            entries = fetch_feed(query)
        except Exception as exc:
            print(f"[warn] Failed to fetch '{query}': {exc}", file=sys.stderr)
            continue

        for entry in entries[:15]:
            url = entry.get('link', '').strip()
            if not url or url in seen:
                continue

            title = clean_title(entry.get('title', '').strip())
            summary = entry.get('summary', '')
            combined = f"{title} {summary}"

            if not INCIDENT_RE.search(combined):
                continue

            pub_dt, date_str = parse_date(entry)
            if pub_dt and pub_dt < cutoff:
                continue

            new_items.append({
                'date': date_str,
                'title': title,
                'url': url,
                'source': source_label(url),
                'high_confidence': bool(HIGH_CONF_RE.search(combined)),
            })
            seen.add(url)

    new_items.sort(key=lambda x: x['date'], reverse=True)

    # Prepend to recent_news and cap length
    data['recent_news'] = (new_items + data.get('recent_news', []))[:RECENT_NEWS_CAP]

    # Auto-advance last_incident when a high-confidence item is newer
    high_conf = [i for i in new_items if i['high_confidence']]
    if high_conf:
        latest_date = high_conf[0]['date']
        current_last = data['last_incident'][:10]
        article_dt = datetime.strptime(latest_date, '%Y-%m-%d').replace(tzinfo=TW)
        recency_cutoff = datetime.now(TW) - timedelta(days=14)
        if latest_date > current_last and article_dt >= recency_cutoff:
            data['last_incident'] = f"{latest_date}T00:00:00+08:00"
            data['last_incident_title'] = f"自動偵測：{high_conf[0]['title']}"
            data['auto_updated'] = True
            print(f"[info] last_incident advanced → {latest_date}")
        else:
            data['auto_updated'] = False
    else:
        data['auto_updated'] = False

    data['last_updated'] = datetime.now(TW).isoformat()

    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(
        f"[done] +{len(new_items)} new items  "
        f"| total recent_news: {len(data['recent_news'])}"
    )


if __name__ == '__main__':
    main()
