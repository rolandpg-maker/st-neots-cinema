"""Update St Neots cinema screenings from the public GoFilm town listing.
Keeps previously observed days so the Friday-to-Thursday week remains browsable.
"""
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

URL = 'https://gofilm.uk/towns/st-neots'
DEST = Path(__file__).resolve().parents[1] / 'docs' / 'showtimes.json'
TZ = ZoneInfo('Europe/London')
DAY_RE = re.compile(r'(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)', re.I)
TIME_RE = re.compile(r'^([01]\d|2[0-3]):[0-5]\d(?:\s+.*)?$')


def scrape():
    response = requests.get(URL, timeout=30, headers={'User-Agent': 'Mozilla/5.0 (compatible; personal-cinema-listings/1.0)'})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    now = datetime.now(TZ)
    listings = {}
    date = None
    movie = None
    for node in soup.find_all(['h2', 'h4', 'a']):
        if node.name == 'h2':
            title = node.get_text(' ', strip=True)
            match = DAY_RE.search(title)
            date = None
            movie = None
            if match:
                day, month = match.groups()
                tentative = datetime.strptime(f'{day} {month} {now.year}', '%d %B %Y').date()
                if (tentative - now.date()).days > 200:
                    tentative = tentative.replace(year=now.year - 1)
                elif (now.date() - tentative).days > 200:
                    tentative = tentative.replace(year=now.year + 1)
                date = tentative.isoformat()
                listings.setdefault(date, [])
        elif node.name == 'h4' and date:
            movie = {'title': node.get_text(' ', strip=True), 'times': []}
            if movie['title']:
                listings[date].append(movie)
        elif node.name == 'a' and date and movie:
            label = node.get_text(' ', strip=True)
            if TIME_RE.fullmatch(label):
                time = label[:5]
                extra = label[5:].strip()
                entry = {'time': time}
                if extra:
                    entry['note'] = extra
                if entry not in movie['times']:
                    movie['times'].append(entry)
    return {d: [m for m in movies if m['times']] for d, movies in listings.items() if movies}


def main():
    previous = {'days': {}}
    if DEST.exists():
        previous = json.loads(DEST.read_text(encoding='utf8'))
    new = scrape()
    if not new or sum(map(len, new.values())) < 5:
        raise RuntimeError('Could not validate cinema listings. Keeping existing data.')
    days = previous.get('days', {})
    # Preserve the previously fetched past days, which disappear from rolling listings.
    days.update(new)
    today = datetime.now(TZ).date()
    days = {k: v for k, v in sorted(days.items()) if -21 <= (datetime.fromisoformat(k).date() - today).days <= 21}
    payload = {'source': URL, 'updated': datetime.now(TZ).isoformat(timespec='minutes'), 'days': days}
    DEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(f'Updated {len(new)} dates; {sum(len(v) for v in days.values())} film-day entries retained.')

if __name__ == '__main__':
    main()
