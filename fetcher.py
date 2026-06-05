"""
RSS 피드에서 최신 기사를 카테고리별로 수집합니다.
이미지 URL, 키워드, 요약을 함께 추출합니다.
"""

import re
import time
import feedparser
from datetime import datetime, timezone, timedelta
from typing import List, Dict

FEEDS = {
    "UX/프로덕트 디자인": [
        # ── 영문 전문지 ──────────────────────────────
        {"url": "https://uxdesign.cc/feed",                       "lang": "en", "source": "UX Collective"},
        {"url": "https://www.nngroup.com/feed/rss/",              "lang": "en", "source": "Nielsen Norman"},
        {"url": "https://alistapart.com/main/feed/",              "lang": "en", "source": "A List Apart"},
        {"url": "https://www.smashingmagazine.com/feed/",         "lang": "en", "source": "Smashing Mag"},
        {"url": "https://www.creativebloq.com/rss.xml",           "lang": "en", "source": "Creative Bloq"},
        {"url": "https://feeds.feedburner.com/uxmovement",        "lang": "en", "source": "UX Movement"},
        {"url": "https://www.fastcompany.com/design/rss",         "lang": "en", "source": "Fast Co Design"},
        # ── 국내 ────────────────────────────────────
        {"url": "https://news.google.com/rss/search?q=UX+디자인+트렌드&hl=ko&gl=KR&ceid=KR:ko",   "lang": "ko", "source": "Google News"},
        {"url": "https://news.google.com/rss/search?q=프로덕트+디자인+서비스&hl=ko&gl=KR&ceid=KR:ko", "lang": "ko", "source": "Google News"},
        {"url": "https://news.google.com/rss/search?q=UI+UX+앱+서비스&hl=ko&gl=KR&ceid=KR:ko",     "lang": "ko", "source": "Google News"},
    ],
    "자동차/모빌리티 테크": [
        # ── 영문 일반 자동차 ──────────────────────────
        {"url": "https://techcrunch.com/category/transportation/feed/",                                          "lang": "en", "source": "TechCrunch",       "ivi": False},
        {"url": "https://electrek.co/feed/",                                                                     "lang": "en", "source": "Electrek",         "ivi": False},
        {"url": "https://www.caranddriver.com/rss/all.xml/",                                                     "lang": "en", "source": "Car and Driver",    "ivi": False},
        {"url": "https://www.autonews.com/arc/outboundfeeds/rss/?outputType=xml",                               "lang": "en", "source": "Automotive News",   "ivi": False},
        {"url": "https://news.google.com/rss/search?q=automotive+software+EV&hl=en&gl=US&ceid=US:en",           "lang": "en", "source": "Google News EN",    "ivi": False},
        # ── 영문 IVI 특화 ─────────────────────────────
        {"url": "https://news.google.com/rss/search?q=IVI+infotainment+automotive&hl=en&gl=US&ceid=US:en",      "lang": "en", "source": "Google News EN",    "ivi": True},
        {"url": "https://news.google.com/rss/search?q=Android+Automotive+AAOS+HMI&hl=en&gl=US&ceid=US:en",     "lang": "en", "source": "Google News EN",    "ivi": True},
        {"url": "https://news.google.com/rss/search?q=in-vehicle+display+cockpit+UX&hl=en&gl=US&ceid=US:en",   "lang": "en", "source": "Google News EN",    "ivi": True},
        # ── 국내 일반 자동차 ──────────────────────────
        {"url": "http://www.autoherald.co.kr/rss/allArticle.xml",                                                "lang": "ko", "source": "오토헤럴드",         "ivi": False},
        {"url": "https://news.google.com/rss/search?q=전기차+자율주행+모빌리티&hl=ko&gl=KR&ceid=KR:ko",            "lang": "ko", "source": "Google News",      "ivi": False},
        # ── 국내 IVI 특화 ─────────────────────────────
        {"url": "https://news.google.com/rss/search?q=차량용+인포테인먼트+IVI+HMI&hl=ko&gl=KR&ceid=KR:ko",        "lang": "ko", "source": "Google News",      "ivi": True},
        {"url": "https://news.google.com/rss/search?q=AAOS+안드로이드+오토모티브+차량용+소프트웨어&hl=ko&gl=KR&ceid=KR:ko", "lang": "ko", "source": "Google News", "ivi": True},
        {"url": "https://news.google.com/rss/search?q=커넥티드카+헤드유닛+차량+디스플레이&hl=ko&gl=KR&ceid=KR:ko",  "lang": "ko", "source": "Google News",      "ivi": True},
    ],
    "IT/테크 트렌드": [
        # ── 영문 전문지 ──────────────────────────────
        {"url": "https://www.wired.com/feed/rss",                        "lang": "en", "source": "Wired"},
        {"url": "https://www.technologyreview.com/feed/",                "lang": "en", "source": "MIT Tech Review"},
        {"url": "https://feeds.arstechnica.com/arstechnica/index",       "lang": "en", "source": "Ars Technica"},
        {"url": "https://feeds.feedburner.com/venturebeat/SZYF",         "lang": "en", "source": "VentureBeat"},
        {"url": "https://techcrunch.com/feed/",                          "lang": "en", "source": "TechCrunch"},
        {"url": "https://www.theverge.com/rss/index.xml",                "lang": "en", "source": "The Verge"},
        {"url": "https://www.fastcompany.com/rss",                       "lang": "en", "source": "Fast Company"},
        {"url": "http://rss.cnn.com/rss/cnn_tech.rss",                   "lang": "en", "source": "CNN Tech"},
        # ── 국내 ────────────────────────────────────
        {"url": "https://www.mk.co.kr/rss/30100041/",                                           "lang": "ko", "source": "매일경제"},
        {"url": "https://news.google.com/rss/search?q=AI+IT+스타트업+기술&hl=ko&gl=KR&ceid=KR:ko",  "lang": "ko", "source": "Google News"},
        {"url": "https://news.google.com/rss/search?q=인공지능+플랫폼+빅테크&hl=ko&gl=KR&ceid=KR:ko", "lang": "ko", "source": "Google News"},
        {"url": "https://news.google.com/rss/search?q=테크+스타트업+IT산업&hl=ko&gl=KR&ceid=KR:ko",  "lang": "ko", "source": "Google News"},
    ],
}

# 카테고리별 관련 키워드 — 제목/요약에 하나라도 포함돼야 통과
CATEGORY_KEYWORDS: Dict[str, Dict[str, List[str]]] = {
    "UX/프로덕트 디자인": {
        "en": ["ux", "user experience", "design", "interface", "usability", "figma",
               "prototype", "wireframe", "accessibility", "design system", "product design",
               "ui ", "interaction design", "user research", "persona", "journey", "heuristic",
               "typography", "visual design", "branding", "creative"],
        "ko": ["디자인", "UX", "사용자", "인터페이스", "경험", "프로덕트", "UI", "와이어프레임",
               "프로토타입", "사용성", "접근성", "시각", "아이덴티티", "브랜딩", "인터랙션",
               "피그마", "서비스디자인"],
    },
    "자동차/모빌리티 테크": {
        "en": ["car", "vehicle", "automotive", "electric", " ev ", "autonomous", "self-driving",
               "mobility", "aaos", "infotainment", "tesla", "rivian", "waymo", "cruise",
               "connected car", "transportation", "truck", "fleet", "charging", "battery",
               "lidar", "radar", "oem", "tier1", "sdv"],
        "ko": ["자동차", "차량", "전기차", "자율주행", "모빌리티", "인포테인먼트", "커넥티드",
               "AAOS", "SDV", "OTA", "차량용", "충전", "배터리", "완성차", "오토", "카",
               "운전", "도로", "교통"],
    },
    "IT/테크 트렌드": {
        "en": ["ai", "artificial intelligence", "tech", "software", "startup", "api",
               "llm", "machine learning", "data", "chip", "gpu", "cloud", "saas",
               "openai", "google", "microsoft", "apple", "meta", "amazon", "nvidia",
               "cybersecurity", "blockchain", "platform", "app", "mobile", "developer",
               "algorithm", "model", "robot", "automation"],
        "ko": ["AI", "인공지능", "소프트웨어", "스타트업", "플랫폼", "클라우드", "데이터",
               "앱", "IT", "반도체", "챗봇", "모델", "빅테크", "테크", "개발자", "알고리즘",
               "자동화", "로봇", "사이버보안", "블록체인"],
    },
}

# 전문 미디어는 필터링 면제 (항상 관련 기사만 다루므로)
TRUSTED_SOURCES = {
    "UX Collective", "Nielsen Norman", "A List Apart", "Smashing Mag",
    "Creative Bloq", "UX Movement", "Fast Co Design",
    "Automotive News", "Car and Driver", "Electrek", "오토헤럴드",
    "MIT Tech Review", "Ars Technica", "VentureBeat",
}


IVI_KEYWORDS = {
    "en": ["ivi", "infotainment", "in-vehicle", "hmi", "head unit", "cockpit", "aaos",
           "android automotive", "carplay", "android auto", "vehicle display", "dashboard ux",
           "connected car", "in-car", "digital cluster"],
    "ko": ["IVI", "인포테인먼트", "차량용", "HMI", "헤드유닛", "AAOS", "안드로이드 오토모티브",
           "카플레이", "안드로이드 오토", "차량 디스플레이", "디지털 클러스터", "커넥티드카"],
}


def is_ivi_article(article: dict) -> bool:
    """기사가 IVI(인포테인먼트/차량 HMI) 관련인지 판단합니다."""
    text = (article["title"] + " " + article["summary"]).lower()
    lang = article["lang"]
    return any(kw.lower() in text for kw in IVI_KEYWORDS.get(lang, []))


def select_automotive(articles: list, total: int = 10, ivi_ratio: float = 0.4) -> list:
    """자동차 기사에서 IVI 40%, 일반 60% 비율로 선택합니다."""
    ivi   = [a for a in articles if a.get("is_ivi")]
    other = [a for a in articles if not a.get("is_ivi")]

    ivi_count   = round(total * ivi_ratio)   # 4
    other_count = total - ivi_count           # 6

    def balance(pool, n):
        ko = [a for a in pool if a["lang"] == "ko"]
        en = [a for a in pool if a["lang"] == "en"]
        half = n // 2
        return ko[:half] + en[:n - half]

    selected = balance(ivi, ivi_count) + balance(other, other_count)

    # 부족하면 남은 풀에서 보충
    if len(selected) < total:
        used = {a["url"] for a in selected}
        extras = [a for a in articles if a["url"] not in used]
        selected += extras[:total - len(selected)]

    selected.sort(key=lambda x: x["date"], reverse=True)
    return selected[:total]


def is_relevant(article: dict, category: str) -> bool:
    """기사 제목+요약이 해당 카테고리 키워드를 포함하는지 확인합니다."""
    if article["source"] in TRUSTED_SOURCES:
        return True

    text = (article["title"] + " " + article["summary"]).lower()
    lang = article["lang"]
    keywords = CATEGORY_KEYWORDS.get(category, {}).get(lang, [])
    return any(kw.lower() in text for kw in keywords)


EN_STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "may",
    "might", "must", "can", "to", "of", "in", "for", "on", "with", "at", "by",
    "from", "up", "into", "and", "or", "but", "if", "as", "that", "this",
    "how", "why", "what", "when", "where", "who", "which", "its", "it", "we",
    "they", "you", "he", "she", "new", "more", "says", "said", "use", "using",
    "used", "just", "also", "now", "get", "make", "one", "two", "three",
    "about", "after", "before", "than", "then", "their", "there", "here",
    "your", "our", "his", "her", "not", "no", "all", "over", "out", "so",
}


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def parse_date(entry) -> datetime:
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return datetime(*val[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return datetime.now(timezone.utc)


def extract_image(entry) -> str:
    """피드 엔트리에서 대표 이미지 URL을 추출합니다."""
    # 1. media:thumbnail
    thumb = getattr(entry, "media_thumbnail", None)
    if thumb and isinstance(thumb, list) and thumb:
        url = thumb[0].get("url", "")
        if url and url.startswith("http"):
            return url

    # 2. media:content
    media = getattr(entry, "media_content", None)
    if media and isinstance(media, list):
        for m in media:
            url = m.get("url", "")
            mtype = m.get("type", "")
            if url and url.startswith("http") and (
                mtype.startswith("image") or
                any(url.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp"))
            ):
                return url

    # 3. enclosures
    for enc in getattr(entry, "enclosures", []):
        if "image" in enc.get("type", ""):
            url = enc.get("href", "")
            if url and url.startswith("http"):
                return url

    # 4. content 블록의 img 태그
    for block in getattr(entry, "content", []):
        match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', block.get("value", ""))
        if match and match.group(1).startswith("http"):
            return match.group(1)

    # 5. summary의 img 태그
    summary_raw = getattr(entry, "summary", "") or ""
    match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', summary_raw)
    if match and match.group(1).startswith("http"):
        return match.group(1)

    return ""


def extract_keywords(title: str, lang: str) -> List[str]:
    """제목에서 대표 키워드 3~4개를 추출합니다."""
    if lang == "en":
        # 대문자로 시작하는 단어 (고유명사) 우선
        proper = re.findall(r'\b([A-Z][a-z]{2,}|[A-Z]{2,10})\b', title)
        # 5글자 이상의 일반 단어
        content = [
            w for w in re.findall(r'\b[a-zA-Z]{5,}\b', title)
            if w.lower() not in EN_STOP_WORDS
        ]
        combined = proper + [w for w in content if w not in proper]
        seen, result = set(), []
        for w in combined:
            wl = w.lower()
            if wl not in seen:
                seen.add(wl)
                result.append(w)
        return result[:4]
    else:
        # 한국어: 2글자 이상 단어 중 의미 있는 것
        words = [w.strip(".,!?:()[]") for w in title.split() if len(w.strip(".,!?:()[]")) >= 2]
        return words[:4]


JUNK_PATTERNS = [
    r"Continue reading on .+»",
    r"Read more.*$",
    r"Click here.*$",
    r"View more.*$",
    r"\[…\]$",
    r"\.{3}$",
]


def extract_summary(entry) -> str:
    """피드 엔트리에서 의미 있는 요약문을 추출합니다."""
    candidates = []

    # content 블록 (가장 풍부한 텍스트)
    for block in getattr(entry, "content", []):
        text = strip_html(block.get("value", "")).strip()
        if text:
            candidates.append(text)

    # summary / description 필드
    raw = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
    text = strip_html(raw).strip()
    if text:
        candidates.append(text)

    # 가장 긴 후보 선택
    best = max(candidates, key=len, default="")

    # 쓸모없는 문구 제거
    for pattern in JUNK_PATTERNS:
        best = re.sub(pattern, "", best, flags=re.IGNORECASE).strip()

    # 80자 미만이면 의미 없는 요약으로 판단
    return best[:400] if len(best) >= 80 else ""


def fetch_feed(config: dict, max_age_hours: int = 72) -> List[Dict]:
    articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)

    try:
        parsed = feedparser.parse(config["url"])
        for entry in parsed.entries[:20]:
            pub_date = parse_date(entry)
            if pub_date < cutoff:
                continue

            title = strip_html(entry.get("title", "")).strip()
            if not title:
                continue

            summary = extract_summary(entry)

            keywords = extract_keywords(title, config["lang"])
            image_url = extract_image(entry)

            article = {
                "title": title,
                "url": entry.get("link", ""),
                "source": config["source"],
                "lang": config["lang"],
                "date": pub_date,
                "summary": summary,
                "keywords": keywords,
                "image": image_url,
                "is_ivi": config.get("ivi", False),
            }
            # 피드에 ivi=True가 없어도 키워드로 재판단
            if not article["is_ivi"]:
                article["is_ivi"] = is_ivi_article(article)
            articles.append(article)
    except Exception as e:
        print(f"  오류 ({config['source']}): {e}")

    return articles


def fetch_all(articles_per_category: int = 10) -> Dict[str, List[Dict]]:
    result = {}

    for category, feeds in FEEDS.items():
        print(f"  [{category}] 수집 중...")
        all_articles = []

        for config in feeds:
            all_articles.extend(fetch_feed(config))
            time.sleep(0.3)

        # 관련성 필터 + 중복 제거
        all_articles = [a for a in all_articles if is_relevant(a, category)]
        all_articles.sort(key=lambda x: x["date"], reverse=True)
        seen_urls, seen_titles, unique = set(), set(), []
        for a in all_articles:
            key = a["url"] or a["title"]
            title_key = a["title"][:40].lower()
            if key not in seen_urls and title_key not in seen_titles:
                seen_urls.add(key)
                seen_titles.add(title_key)
                unique.append(a)

        # 자동차 카테고리는 IVI 40% 비율 적용
        if category == "자동차/모빌리티 테크":
            selected = select_automotive(unique, total=articles_per_category)
        else:
            ko = [a for a in unique if a["lang"] == "ko"]
            en = [a for a in unique if a["lang"] == "en"]
            half = articles_per_category // 2
            selected = ko[:half] + en[:articles_per_category - half]
            selected.sort(key=lambda x: x["date"], reverse=True)

        result[category] = selected
        ivi_cnt = len([a for a in selected if a.get("is_ivi")])
        kr_cnt  = len([a for a in selected if a["lang"] == "ko"])
        en_cnt  = len([a for a in selected if a["lang"] == "en"])
        ivi_str = f", IVI {ivi_cnt}개" if category == "자동차/모빌리티 테크" else ""
        print(f"    → {len(selected)}개 (KR {kr_cnt}, EN {en_cnt}{ivi_str})")

    return result
