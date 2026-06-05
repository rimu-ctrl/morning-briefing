#!/usr/bin/env python3
"""
모닝 브리핑 생성기
- docs/index.html      : 오늘의 기사 + 영어 패널 (GitHub Pages)
- docs/vocab_all.html  : 전체 단어 아카이브
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from fetcher import fetch_all
from summarizer import generate_summaries_batch
from renderer import render_html
from vocabulary import WORDS, IDIOMS

PROJECT_DIR   = Path(__file__).parent
DOCS_DIR      = PROJECT_DIR / "docs"
BRIEFING_PATH = DOCS_DIR / "index.html"
ARCHIVE_PATH  = DOCS_DIR / "vocab_all.html"
KEYWORD       = "okrimu"


# ── 아카이브 페이지 생성 ──────────────────────────────────────────────────────

def render_vocab_archive() -> str:
    all_words  = sorted(WORDS,  key=lambda x: x["word"].lower())
    all_idioms = sorted(IDIOMS, key=lambda x: x["word"].lower())

    def items_html(items):
        html = ""
        for w in items:
            wid = w["word"].replace(" ", "_").replace("/", "_")
            html += f"""
          <li class="av" data-word="{w['word']}">
            <div class="av-top">
              <span class="av-word">{w['word']}</span>
              <span class="av-type">{w['type']}</span>
              <div class="av-actions">
                <button class="av-btn star" onclick="toggleStar('{wid}')" title="복습">☆</button>
                <button class="av-btn check" onclick="toggleCheck('{wid}')" title="암기완료">○</button>
              </div>
            </div>
            <p class="av-meaning">{w['meaning']}</p>
            <p class="av-example">"{w['example']}"</p>
          </li>"""
        return html

    words_html  = items_html(all_words)
    idioms_html = items_html(all_idioms)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>영어 아카이브</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Pretendard", "Noto Sans KR", sans-serif;
            background: #f0f2f5; color: #1a1a2e; }}
    /* 잠금 화면 */
    #lock-screen {{
      position: fixed; inset: 0; z-index: 9999;
      background: linear-gradient(135deg, #0d1117 0%, #1a1a2e 60%, #16213e 100%);
      display: flex; align-items: center; justify-content: center;
    }}
    .lock-box {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
                 border-radius: 20px; padding: 2.5rem 2rem; text-align: center; width: 320px; }}
    .lock-icon {{ font-size: 2.5rem; margin-bottom: 1rem; }}
    .lock-title {{ color: #fff; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.4rem; }}
    .lock-sub {{ color: rgba(255,255,255,0.4); font-size: 0.78rem; margin-bottom: 1.5rem; }}
    .lock-input {{ width: 100%; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
                   border-radius: 10px; color: #fff; font-size: 1rem; padding: 0.7rem 1rem;
                   text-align: center; letter-spacing: 0.1em; outline: none; transition: border-color 0.2s; }}
    .lock-input:focus {{ border-color: #4361ee; }}
    .lock-input.error {{ border-color: #e63946; animation: shake 0.3s; }}
    .lock-btn {{ margin-top: 1rem; width: 100%; background: #4361ee; border: none; border-radius: 10px;
                 color: #fff; font-size: 0.95rem; font-weight: 700; padding: 0.75rem;
                 cursor: pointer; transition: background 0.2s; }}
    .lock-btn:hover {{ background: #3451d1; }}
    @keyframes shake {{ 0%,100%{{transform:translateX(0)}} 25%{{transform:translateX(-6px)}} 75%{{transform:translateX(6px)}} }}
    header {{ background: linear-gradient(135deg, #0d1117, #4361ee); color: #fff; padding: 1.8rem 2rem; }}
    .hd-top {{ display: flex; align-items: center; gap: 1rem; }}
    .back-btn {{ color: rgba(255,255,255,0.7); text-decoration: none; font-size: 0.8rem;
                 border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; padding: 4px 12px; }}
    .back-btn:hover {{ background: rgba(255,255,255,0.1); }}
    h1 {{ font-size: 1.5rem; font-weight: 800; }}
    .hd-sub {{ font-size: 0.8rem; opacity: 0.55; margin-top: 0.4rem; }}
    .stats {{ display: flex; gap: 1.5rem; margin-top: 1rem; flex-wrap: wrap; }}
    .stat {{ font-size: 0.78rem; opacity: 0.7; }}
    .stat span {{ font-weight: 700; opacity: 1; }}
    .filters {{ padding: 1rem 2rem; display: flex; gap: 0.5rem; flex-wrap: wrap; background: #fff;
                border-bottom: 1px solid #e5e7eb; }}
    .filter-btn {{ border: 1px solid #e5e7eb; background: #fff; border-radius: 20px;
                   padding: 4px 14px; font-size: 0.75rem; cursor: pointer; transition: all 0.15s; }}
    .filter-btn:hover, .filter-btn.active {{ background: #4361ee; color: #fff; border-color: #4361ee; }}
    main {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }}
    .section-title {{ font-size: 0.85rem; font-weight: 700; color: #9ca3af; text-transform: uppercase;
                      letter-spacing: 0.08em; margin: 2rem 0 0.8rem; padding-bottom: 0.5rem;
                      border-bottom: 2px solid #e5e7eb; }}
    .section-title:first-child {{ margin-top: 0; }}
    .av-list {{ list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }}
    .av {{ background: #fff; border-radius: 12px; padding: 0.9rem 1.1rem;
           border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 1px 3px rgba(0,0,0,0.04); transition: background 0.15s; }}
    .av.is-learned {{ background: #f0fdf4; border-color: #bbf7d0; }}
    .av.is-starred {{ background: #fffbeb; border-color: #fde68a; }}
    .av.hidden {{ display: none; }}
    .av-top {{ display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.3rem; }}
    .av-word {{ font-size: 0.95rem; font-weight: 700; flex: 1; }}
    .av-type {{ font-size: 0.62rem; color: #4361ee; background: #eef0fd; padding: 2px 7px; border-radius: 4px; font-weight: 600; flex-shrink: 0; }}
    .av-actions {{ display: flex; gap: 0.3rem; }}
    .av-btn {{ background: none; border: none; cursor: pointer; font-size: 1rem; color: #d1d5db; transition: color 0.15s; padding: 0 2px; }}
    .av-btn:hover {{ color: #6b7280; }}
    .av.is-starred .av-btn.star {{ color: #f59e0b; }}
    .av.is-learned .av-btn.check {{ color: #22c55e; }}
    .av-meaning {{ font-size: 0.82rem; color: #374151; font-weight: 500; margin-bottom: 0.25rem; }}
    .av-example {{ font-size: 0.76rem; color: #9ca3af; line-height: 1.5; font-style: italic; }}
    footer {{ text-align: center; padding: 3rem; font-size: 0.73rem; color: #bbb; }}
  </style>
</head>
<body>

<div id="lock-screen">
  <div class="lock-box">
    <div class="lock-icon">📚</div>
    <p class="lock-title">영어 아카이브</p>
    <p class="lock-sub">키워드를 입력하세요</p>
    <input type="password" id="lock-input" class="lock-input"
           placeholder="keyword" autocomplete="off"
           onkeydown="if(event.key==='Enter')unlock()">
    <button class="lock-btn" onclick="unlock()">열기</button>
  </div>
</div>
<script>
  (function(){{
    const KEY='{KEYWORD}', AUTH='brief_auth';
    if(localStorage.getItem(AUTH)==='1') document.getElementById('lock-screen').style.display='none';
    window.unlock=function(){{
      const inp=document.getElementById('lock-input');
      if(inp.value===KEY){{ localStorage.setItem(AUTH,'1'); document.getElementById('lock-screen').style.display='none'; }}
      else {{ inp.classList.add('error'); inp.value=''; setTimeout(()=>inp.classList.remove('error'),400); }}
    }};
  }})();
</script>

<header>
  <div class="hd-top">
    <a href="index.html" class="back-btn">← 오늘의 브리핑</a>
    <h1>📚 영어 아카이브</h1>
  </div>
  <p class="hd-sub">전체 단어 · 알파벳 순 정렬</p>
  <div class="stats">
    <p class="stat">단어 <span>{len(all_words)}</span>개</p>
    <p class="stat">숙어/표현 <span>{len(all_idioms)}</span>개</p>
    <p class="stat">암기완료 <span id="learned-count">0</span>개</p>
    <p class="stat">복습중 <span id="starred-count">0</span>개</p>
  </div>
</header>

<div class="filters">
  <button class="filter-btn active" onclick="setFilter('all')">전체</button>
  <button class="filter-btn" onclick="setFilter('starred')">★ 복습중</button>
  <button class="filter-btn" onclick="setFilter('learned')">✓ 암기완료</button>
  <button class="filter-btn" onclick="setFilter('todo')">미완료만</button>
</div>

<main>
  <p class="section-title">단어 ({len(all_words)})</p>
  <ul class="av-list">{words_html}
  </ul>
  <p class="section-title">숙어 &amp; 표현 ({len(all_idioms)})</p>
  <ul class="av-list">{idioms_html}
  </ul>
</main>

<footer>총 {len(all_words) + len(all_idioms)}개 · 알파벳 순</footer>

<script>
  const STATUS_KEY = 'vocabStatus';
  let currentFilter = 'all';
  function getStatus() {{ return JSON.parse(localStorage.getItem(STATUS_KEY) || '{{}}'); }}
  function saveStatus(s) {{ localStorage.setItem(STATUS_KEY, JSON.stringify(s)); }}
  function toggleStar(wid) {{ const s=getStatus(); s[wid]=s[wid]==='starred'?null:'starred'; if(!s[wid])delete s[wid]; saveStatus(s); applyStatus(); }}
  function toggleCheck(wid) {{ const s=getStatus(); s[wid]=s[wid]==='learned'?null:'learned'; if(!s[wid])delete s[wid]; saveStatus(s); applyStatus(); }}
  function setFilter(f) {{ currentFilter=f; document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active')); event.target.classList.add('active'); applyStatus(); }}
  function applyStatus() {{
    const s=getStatus(); let lc=0, sc=0;
    document.querySelectorAll('.av').forEach(el=>{{
      const wid=el.dataset.word.replace(/ /g,'_').replace(/\//g,'_');
      const st=s[wid];
      el.classList.toggle('is-starred',st==='starred'); el.classList.toggle('is-learned',st==='learned');
      el.querySelector('.star').textContent=st==='starred'?'★':'☆';
      el.querySelector('.check').textContent=st==='learned'?'●':'○';
      if(st==='learned')lc++; if(st==='starred')sc++;
      let show=true;
      if(currentFilter==='starred')show=st==='starred';
      else if(currentFilter==='learned')show=st==='learned';
      else if(currentFilter==='todo')show=!st;
      el.classList.toggle('hidden',!show);
    }});
    document.getElementById('learned-count').textContent=lc;
    document.getElementById('starred-count').textContent=sc;
  }}
  document.addEventListener('DOMContentLoaded', applyStatus);
</script>
</body>
</html>"""


# ── GitHub push ───────────────────────────────────────────────────────────────

def git_push():
    try:
        subprocess.run(["git", "add", "docs/"], cwd=PROJECT_DIR, check=True)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        subprocess.run(
            ["git", "commit", "-m", f"briefing: {date_str}"],
            cwd=PROJECT_DIR, check=True
        )
        subprocess.run(["git", "push"], cwd=PROJECT_DIR, check=True)
        print("✓ GitHub push 완료")
    except subprocess.CalledProcessError as e:
        print(f"  GitHub push 실패: {e}")


# ── 메인 ────────────────────────────────────────────────────────────────────

def main():
    load_dotenv()

    print("=" * 40)
    print("  모닝 브리핑 생성 시작")
    print("=" * 40)

    DOCS_DIR.mkdir(exist_ok=True)

    articles_by_cat = fetch_all(articles_per_category=10)

    for cat, articles in articles_by_cat.items():
        articles_by_cat[cat] = generate_summaries_batch(articles)

    now = datetime.now()

    briefing_html = render_html(articles_by_cat, now, keyword=KEYWORD)
    BRIEFING_PATH.write_text(briefing_html, encoding="utf-8")

    archive_html = render_vocab_archive()
    ARCHIVE_PATH.write_text(archive_html, encoding="utf-8")

    total = sum(len(v) for v in articles_by_cat.values())
    print(f"\n✓ 기사 {total}개 생성")
    print(f"✓ 브리핑  → {BRIEFING_PATH}")
    print(f"✓ 아카이브 → {ARCHIVE_PATH}")

    git_push()

    os.system(f'open "{BRIEFING_PATH}"')


if __name__ == "__main__":
    main()
