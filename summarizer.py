"""
Claude Haiku API로 기사의 한국어 핵심 요약(5줄 이내)을 생성합니다.
URL 기반 파일 캐시를 사용해 동일 기사는 재생성하지 않습니다.
ANTHROPIC_API_KEY가 없으면 조용히 빈 문자열을 반환합니다.
"""

import os
import json
import hashlib
from pathlib import Path

CACHE_PATH = Path(__file__).parent / ".summary_cache.json"


def _load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_cache(cache: dict):
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def _cache_key(url: str, title: str) -> str:
    return hashlib.md5((url or title).encode()).hexdigest()


def generate_korean_summary(title: str, summary: str, url: str = "") -> str:
    """
    기사 제목+요약을 받아 한국어 핵심 요약을 반환합니다.
    API 키가 없거나 실패 시 빈 문자열 반환.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return ""

    cache = _load_cache()
    key = _cache_key(url, title)
    if key in cache:
        return cache[key]

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        content_for_summary = f"제목: {title}"
        if summary and len(summary) > 50:
            content_for_summary += f"\n내용: {summary[:600]}"

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            messages=[{
                "role": "user",
                "content": (
                    "다음 기사의 핵심을 한국어로 간결하게 요약해주세요.\n"
                    "- 5줄 이내의 bullet point 형식\n"
                    "- 각 줄은 '• '로 시작\n"
                    "- 핵심 사실과 인사이트 위주\n"
                    "- 군더더기 없이 간결하게\n\n"
                    f"{content_for_summary}"
                ),
            }],
        )
        result = message.content[0].text.strip()

        cache[key] = result
        _save_cache(cache)
        return result

    except Exception as e:
        print(f"  [요약 오류] {e}")
        return ""


def generate_summaries_batch(articles: list) -> list:
    """articles 리스트에 korean_summary 필드를 추가해 반환합니다."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        for a in articles:
            a["korean_summary"] = ""
        return articles

    print("  한국어 요약 생성 중...")
    for a in articles:
        a["korean_summary"] = generate_korean_summary(
            a.get("title", ""),
            a.get("summary", ""),
            a.get("url", ""),
        )
    return articles
