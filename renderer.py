"""
수집된 기사를 모닝 브리핑 HTML 페이지로 렌더링합니다.
카드 레이아웃: 대표 이미지 → 메타 → 제목 → 키워드 → 요약
"""

from datetime import datetime, timezone
from typing import Dict, List

from vocabulary import get_daily_words

CATEGORY_META = {
    "UX/프로덕트 디자인":   {"color": "#4361ee", "gradient": "135deg, #4361ee, #7209b7", "emoji": "🎨"},
    "자동차/모빌리티 테크": {"color": "#0a9396", "gradient": "135deg, #0a9396, #005f73", "emoji": "🚗"},
    "IT/테크 트렌드":       {"color": "#7209b7", "gradient": "135deg, #7209b7, #3a0ca3", "emoji": "💻"},
}

WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]


def time_ago(dt: datetime) -> str:
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = now - dt
    mins = int(diff.total_seconds() / 60)
    if mins < 60:
        return f"{mins}분 전"
    hours = mins // 60
    if hours < 24:
        return f"{hours}시간 전"
    return f"{hours // 24}일 전"


def render_card(article: dict, category: str) -> str:
    lang_label = "KR" if article["lang"] == "ko" else "EN"
    lang_color = "#e63946" if article["lang"] == "ko" else "#457b9d"
    gradient = CATEGORY_META.get(category, {}).get("gradient", "135deg, #666, #333")
    emoji = CATEGORY_META.get(category, {}).get("emoji", "📰")
    ivi_badge = '<span class="ivi-badge">IVI</span>' if article.get("is_ivi") else ""

    # 이미지 영역
    if article.get("image"):
        img_html = f"""<div class="card-img">
        <img src="{article['image']}" alt="" loading="lazy"
             onerror="this.parentElement.innerHTML='<span class=\\'ph-emoji\\'>{emoji}</span>';this.parentElement.style.background='linear-gradient({gradient})'">
      </div>"""
    else:
        img_html = f"""<div class="card-img no-img" style="background:linear-gradient({gradient})">
        <span class="ph-emoji">{emoji}</span>
      </div>"""

    # 키워드 태그
    keywords_html = ""
    if article.get("keywords"):
        tags = "".join(f'<span class="kw">#{kw}</span>' for kw in article["keywords"])
        keywords_html = f'<div class="keywords">{tags}</div>'

    # 영문 요약
    summary_html = ""
    if article.get("summary"):
        summary_html = f'<p class="summary">{article["summary"]}</p>'

    # 한국어 핵심 요약
    kr_summary_html = ""
    if article.get("korean_summary"):
        lines = [l.strip() for l in article["korean_summary"].split("\n") if l.strip()]
        bullets = "".join(f"<li>{l.lstrip('•·-– ').strip()}</li>" for l in lines[:5])
        kr_summary_html = f"""
        <div class="kr-summary">
          <p class="kr-label">🇰🇷 핵심 요약</p>
          <ul class="kr-bullets">{bullets}</ul>
        </div>"""

    return f"""
      <div class="article-unit">
        <a href="{article['url']}" class="card" target="_blank" rel="noopener noreferrer">
          {img_html}
          <div class="card-body">
            <div class="card-meta">
              <span class="lang" style="background:{lang_color}">{lang_label}</span>
              {ivi_badge}
              <span class="source">{article['source']}</span>
              <span class="ago">{time_ago(article['date'])}</span>
            </div>
            <p class="card-title">{article['title']}</p>
            {keywords_html}
            {summary_html}
          </div>
        </a>
        {kr_summary_html}
      </div>"""


def _vocab_items_html(items: list, offset: int = 0) -> str:
    html = ""
    for i, w in enumerate(items, offset + 1):
        wid = w["word"].replace(" ", "_").replace("/", "_")
        html += f"""
        <li class="vi" data-word="{w['word']}">
          <div class="vi-top">
            <span class="vi-num">{i:02d}</span>
            <span class="vi-word">{w['word']}</span>
            <span class="vi-type">{w['type']}</span>
            <div class="vi-actions">
              <button class="vi-btn star" onclick="toggleStar('{wid}')" title="복습 표시">☆</button>
              <button class="vi-btn check" onclick="toggleCheck('{wid}')" title="암기 완료">○</button>
            </div>
          </div>
          <p class="vi-meaning">{w['meaning']}</p>
          <p class="vi-example">"{w['example']}"</p>
        </li>"""
    return html


def render_vocab_panel(generated_at: datetime) -> str:
    daily = get_daily_words(generated_at.date())
    words_html  = _vocab_items_html(daily["words"], offset=0)
    idioms_html = _vocab_items_html(daily["idioms"], offset=20)

    return f"""
      <aside class="vocab-panel">
        <div class="vocab-head">
          <span class="vocab-icon">📚</span>
          <div style="flex:1">
            <p class="vocab-title">오늘의 영어</p>
            <p class="vocab-sub">단어 20 · 숙어 10</p>
          </div>
          <a href="vocab_all.html" class="vocab-archive-btn" target="_blank">전체 보기 →</a>
        </div>

        <div class="vocab-section-label">📖 단어 (20)</div>
        <ol class="vocab-list">{words_html}
        </ol>

        <div class="vocab-section-label">💬 숙어 &amp; 표현 (10)</div>
        <ol class="vocab-list">{idioms_html}
        </ol>
      </aside>

      <script>
        const STATUS_KEY = 'vocabStatus';
        function getStatus() {{
          return JSON.parse(localStorage.getItem(STATUS_KEY) || '{{}}');
        }}
        function saveStatus(s) {{
          localStorage.setItem(STATUS_KEY, JSON.stringify(s));
        }}
        function toggleStar(wid) {{
          const s = getStatus();
          s[wid] = s[wid] === 'starred' ? null : 'starred';
          if (!s[wid]) delete s[wid];
          saveStatus(s); applyStatus();
        }}
        function toggleCheck(wid) {{
          const s = getStatus();
          s[wid] = s[wid] === 'learned' ? null : 'learned';
          if (!s[wid]) delete s[wid];
          saveStatus(s); applyStatus();
        }}
        function applyStatus() {{
          const s = getStatus();
          document.querySelectorAll('.vi').forEach(el => {{
            const wid = el.dataset.word.replace(/ /g,'_').replace(/\\//g,'_');
            const status = s[wid];
            el.classList.toggle('is-starred',  status === 'starred');
            el.classList.toggle('is-learned',  status === 'learned');
            el.querySelector('.star').textContent = status === 'starred' ? '★' : '☆';
            el.querySelector('.check').textContent = status === 'learned' ? '●' : '○';
          }});
        }}
        document.addEventListener('DOMContentLoaded', applyStatus);
      </script>"""


def render_html(articles_by_category: Dict[str, List[dict]], generated_at: datetime, keyword: str = "okrimu") -> str:
    month = generated_at.month
    day = generated_at.day
    weekday = WEEKDAYS[generated_at.weekday()]
    time_str = generated_at.strftime("%H:%M")
    total = sum(len(v) for v in articles_by_category.values())

    sections_html = ""
    for category, articles in articles_by_category.items():
        meta = CATEGORY_META.get(category, {"color": "#333", "emoji": "📰"})
        color = meta["color"]
        emoji = meta["emoji"]
        cards_html = "".join(render_card(a, category) for a in articles) if articles \
            else '<p class="empty">오늘 새 기사가 없습니다.</p>'
        sections_html += f"""
    <section class="section">
      <h2 class="section-title" style="color:{color}">
        <span class="section-bar" style="background:{color}"></span>
        {emoji} {category}
        <span class="section-count">{len(articles)}개</span>
      </h2>
      <div class="grid">{cards_html}
      </div>
    </section>"""

    vocab_html = render_vocab_panel(generated_at)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>모닝 브리핑 — {generated_at.year}.{month:02d}.{day:02d}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Pretendard", "Noto Sans KR", "Segoe UI", sans-serif;
      background: #f0f2f5;
      color: #1a1a2e;
    }}

    /* ── 헤더 ── */
    header {{
      background: linear-gradient(135deg, #0d1117 0%, #1a1a2e 60%, #16213e 100%);
      color: #fff;
      padding: 2.5rem 2rem 2rem;
      text-align: center;
    }}
    .header-label {{ font-size: 0.68rem; letter-spacing: 0.35em; text-transform: uppercase; opacity: 0.45; margin-bottom: 0.7rem; }}
    .header-date {{ font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em; }}
    .header-date .wd {{ font-weight: 300; opacity: 0.6; margin-left: 0.4rem; }}
    .header-tags {{ margin-top: 1rem; display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap; }}
    .tag {{ background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 0.3rem 0.9rem; font-size: 0.73rem; color: rgba(255,255,255,0.65); }}
    .header-count {{ margin-top: 1.1rem; font-size: 0.75rem; opacity: 0.35; }}

    /* ── 2단 레이아웃 ── */
    .layout {{
      max-width: 1500px;
      margin: 0 auto;
      padding: 2rem 1.5rem 5rem;
      display: grid;
      grid-template-columns: 1fr 300px;
      gap: 1.8rem;
      align-items: start;
    }}

    /* ── 기사 영역 ── */
    .section {{ margin-bottom: 2.8rem; }}
    .section-title {{
      display: flex; align-items: center; gap: 0.55rem;
      font-size: 0.95rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 0.07em;
      margin-bottom: 1.1rem;
    }}
    .section-bar {{ display: inline-block; width: 4px; height: 16px; border-radius: 2px; flex-shrink: 0; }}
    .section-count {{ margin-left: auto; font-size: 0.72rem; font-weight: 500; opacity: 0.5; letter-spacing: 0; }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
      gap: 1rem;
    }}

    /* ── 카드 ── */
    .card {{
      background: #fff; border-radius: 14px; overflow: hidden;
      text-decoration: none; color: inherit; display: flex; flex-direction: column;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 14px rgba(0,0,0,0.05);
      border: 1px solid rgba(0,0,0,0.04);
      transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}
    .card:hover {{ transform: translateY(-4px); box-shadow: 0 6px 16px rgba(0,0,0,0.1), 0 16px 40px rgba(0,0,0,0.08); }}

    .card-img {{ width: 100%; height: 140px; overflow: hidden; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
    .card-img img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .card-img.no-img {{ background: linear-gradient(135deg, #ccc, #888); }}
    .ph-emoji {{ font-size: 2.2rem; opacity: 0.6; }}

    /* ── 기사 유닛 (카드 + 한국어 요약) ── */
    .article-unit {{ display: flex; flex-direction: column; }}
    .card-body {{ padding: 0.75rem 1rem 0.9rem; display: flex; flex-direction: column; gap: 0.4rem; flex: 1; }}
    .card-meta {{ display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap; }}
    .lang {{ color: #fff; font-size: 0.58rem; font-weight: 800; padding: 2px 6px; border-radius: 4px; letter-spacing: 0.04em; flex-shrink: 0; }}
    .ivi-badge {{ background: #0a9396; color: #fff; font-size: 0.58rem; font-weight: 800; padding: 2px 6px; border-radius: 4px; flex-shrink: 0; }}
    .source {{ font-size: 0.73rem; color: #999; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .ago {{ font-size: 0.7rem; color: #bbb; margin-left: auto; white-space: nowrap; flex-shrink: 0; }}
    .card-title {{ font-size: 0.88rem; font-weight: 650; line-height: 1.5; color: #1a1a2e; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
    .keywords {{ display: flex; flex-wrap: wrap; gap: 0.3rem; }}
    .kw {{ font-size: 0.68rem; font-weight: 600; color: #888; background: #f3f4f6; border-radius: 4px; padding: 2px 7px; }}
    .summary {{ font-size: 0.78rem; color: #6b7280; line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
    .empty {{ color: #bbb; font-size: 0.85rem; }}

    /* ── 한국어 핵심 요약 ── */
    .kr-summary {{
      background: #f8faff;
      border: 1px solid #e0e7ff;
      border-top: none;
      border-radius: 0 0 14px 14px;
      padding: 0.7rem 1rem 0.85rem;
    }}
    .kr-label {{ font-size: 0.68rem; font-weight: 700; color: #4361ee; margin-bottom: 0.4rem; letter-spacing: 0.03em; }}
    .kr-bullets {{ list-style: none; display: flex; flex-direction: column; gap: 0.25rem; }}
    .kr-bullets li {{ font-size: 0.75rem; color: #374151; line-height: 1.55; padding-left: 0.9rem; position: relative; }}
    .kr-bullets li::before {{ content: "•"; position: absolute; left: 0; color: #4361ee; }}

    /* ── 영어 패널 ── */
    .vocab-panel {{
      position: sticky; top: 1.5rem;
      background: #fff; border-radius: 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 14px rgba(0,0,0,0.05);
      border: 1px solid rgba(0,0,0,0.04); overflow: hidden;
    }}
    .vocab-head {{
      display: flex; align-items: center; gap: 0.75rem;
      padding: 1rem 1.2rem;
      background: linear-gradient(135deg, #1a1a2e, #4361ee); color: #fff;
    }}
    .vocab-icon {{ font-size: 1.4rem; }}
    .vocab-title {{ font-size: 0.88rem; font-weight: 700; }}
    .vocab-sub {{ font-size: 0.68rem; opacity: 0.6; margin-top: 1px; }}
    .vocab-archive-btn {{
      font-size: 0.68rem; color: rgba(255,255,255,0.75); text-decoration: none;
      border: 1px solid rgba(255,255,255,0.25); border-radius: 20px;
      padding: 3px 10px; white-space: nowrap; flex-shrink: 0;
      transition: background 0.15s;
    }}
    .vocab-archive-btn:hover {{ background: rgba(255,255,255,0.15); }}
    .vocab-section-label {{
      font-size: 0.68rem; font-weight: 700; color: #9ca3af;
      letter-spacing: 0.08em; text-transform: uppercase;
      padding: 0.6rem 1.2rem 0.3rem;
      background: #f9fafb; border-top: 1px solid #f3f4f6;
    }}
    .vocab-list {{ list-style: none; padding: 0; }}
    .vocab-list::-webkit-scrollbar {{ width: 4px; }}
    .vocab-list::-webkit-scrollbar-thumb {{ background: #e5e7eb; border-radius: 2px; }}

    .vi {{ padding: 0.65rem 1.2rem; border-bottom: 1px solid #f3f4f6; transition: background 0.15s; }}
    .vi:last-child {{ border-bottom: none; }}
    .vi.is-learned {{ background: #f0fdf4; }}
    .vi.is-starred {{ background: #fffbeb; }}
    .vi-top {{ display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.15rem; }}
    .vi-num {{ font-size: 0.6rem; color: #d1d5db; font-weight: 700; width: 1.1rem; flex-shrink: 0; }}
    .vi-word {{ font-size: 0.86rem; font-weight: 700; color: #1a1a2e; flex: 1; }}
    .vi-type {{ font-size: 0.6rem; color: #4361ee; background: #eef0fd; padding: 1px 5px; border-radius: 3px; font-weight: 600; flex-shrink: 0; }}
    .vi-actions {{ display: flex; gap: 0.25rem; margin-left: 0.3rem; }}
    .vi-btn {{
      background: none; border: none; cursor: pointer;
      font-size: 0.85rem; line-height: 1; padding: 0 2px;
      color: #d1d5db; transition: color 0.15s;
    }}
    .vi-btn:hover {{ color: #6b7280; }}
    .vi.is-starred .vi-btn.star {{ color: #f59e0b; }}
    .vi.is-learned .vi-btn.check {{ color: #22c55e; }}
    .vi-meaning {{ font-size: 0.76rem; color: #374151; font-weight: 500; margin-bottom: 0.2rem; }}
    .vi-example {{ font-size: 0.71rem; color: #9ca3af; line-height: 1.5; font-style: italic; }}

    /* ── 잠금 화면 ── */
    #lock-screen {{
      position: fixed; inset: 0; z-index: 9999;
      background: linear-gradient(135deg, #0d1117 0%, #1a1a2e 60%, #16213e 100%);
      display: flex; align-items: center; justify-content: center;
    }}
    .lock-box {{
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 20px; padding: 2.5rem 2rem;
      text-align: center; width: 320px;
    }}
    .lock-icon {{ font-size: 2.5rem; margin-bottom: 1rem; }}
    .lock-title {{ color: #fff; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.4rem; }}
    .lock-sub {{ color: rgba(255,255,255,0.4); font-size: 0.78rem; margin-bottom: 1.5rem; }}
    .lock-input {{
      width: 100%; background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.15); border-radius: 10px;
      color: #fff; font-size: 1rem; padding: 0.7rem 1rem;
      text-align: center; letter-spacing: 0.1em; outline: none;
      transition: border-color 0.2s;
    }}
    .lock-input:focus {{ border-color: #4361ee; }}
    .lock-input.error {{ border-color: #e63946; animation: shake 0.3s; }}
    .lock-btn {{
      margin-top: 1rem; width: 100%; background: #4361ee;
      border: none; border-radius: 10px; color: #fff;
      font-size: 0.95rem; font-weight: 700; padding: 0.75rem;
      cursor: pointer; transition: background 0.2s;
    }}
    .lock-btn:hover {{ background: #3451d1; }}
    @keyframes shake {{
      0%,100%{{transform:translateX(0)}} 25%{{transform:translateX(-6px)}} 75%{{transform:translateX(6px)}}
    }}

    /* ── 푸터 ── */
    footer {{ text-align: center; padding: 2rem; font-size: 0.73rem; color: #bbb; grid-column: 1 / -1; }}

    @media (max-width: 900px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .vocab-panel {{ position: static; }}
    }}
    @media (max-width: 600px) {{
      .header-date {{ font-size: 1.6rem; }}
      .grid {{ grid-template-columns: 1fr 1fr; }}
    }}
    @media (max-width: 420px) {{
      .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

<div id="lock-screen">
  <div class="lock-box">
    <div class="lock-icon">☀️</div>
    <p class="lock-title">Morning Briefing</p>
    <p class="lock-sub">키워드를 입력하세요</p>
    <input type="password" id="lock-input" class="lock-input"
           placeholder="keyword" autocomplete="off"
           onkeydown="if(event.key==='Enter')unlock()">
    <button class="lock-btn" onclick="unlock()">열기</button>
  </div>
</div>

<script>
  (function(){{
    const KEY = 'brief_auth';
    const KEYWORD = '{keyword}';
    if(localStorage.getItem(KEY) === '1') {{
      document.getElementById('lock-screen').style.display = 'none';
    }}
    window.unlock = function(){{
      const inp = document.getElementById('lock-input');
      if(inp.value === KEYWORD){{
        localStorage.setItem(KEY, '1');
        document.getElementById('lock-screen').style.display = 'none';
      }} else {{
        inp.classList.add('error');
        inp.value = '';
        setTimeout(()=>inp.classList.remove('error'), 400);
      }}
    }};
  }})();
</script>

<header>
  <p class="header-label">☀ Morning Briefing</p>
  <div class="header-date">
    {generated_at.year}년 {month}월 {day}일<span class="wd">{weekday}요일</span>
  </div>
  <div class="header-tags">
    <span class="tag">🎨 UX/프로덕트</span>
    <span class="tag">🚗 자동차 테크</span>
    <span class="tag">💻 IT 트렌드</span>
    <span class="tag">📚 영어</span>
  </div>
  <p class="header-count">기사 {total}개 · {time_str} 업데이트</p>
</header>

<div class="layout">
  <div class="articles">{sections_html}
  </div>
  {vocab_html}
  <footer>자동 생성 · {generated_at.year}.{month:02d}.{day:02d} {time_str}</footer>
</div>

</body>
</html>"""
