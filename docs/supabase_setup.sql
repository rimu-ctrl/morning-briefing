-- ── 보관/메모 데이터를 저장할 테이블 ──────────────────────────
create table if not exists saved_articles (
  id bigint generated always as identity primary key,
  article_url text not null unique,
  title text,
  bookmarked boolean not null default false,
  memo text not null default '',
  updated_at timestamptz not null default now()
);

alter table saved_articles enable row level security;

create policy "anon can read saved_articles"
  on saved_articles for select to anon using (true);
create policy "anon can insert saved_articles"
  on saved_articles for insert to anon with check (true);
create policy "anon can update saved_articles"
  on saved_articles for update to anon using (true);
create policy "anon can delete saved_articles"
  on saved_articles for delete to anon using (true);


-- ── 영어 단어장 별표/암기완료 상태를 저장할 테이블 ──────────────
-- (기존 vocab_all.html localStorage 데이터를 이관)
create table if not exists vocab_status (
  id bigint generated always as identity primary key,
  word_id text not null unique,
  starred boolean not null default false,
  learned boolean not null default false,
  updated_at timestamptz not null default now()
);

alter table vocab_status enable row level security;

create policy "anon can read vocab_status"
  on vocab_status for select to anon using (true);
create policy "anon can insert vocab_status"
  on vocab_status for insert to anon with check (true);
create policy "anon can update vocab_status"
  on vocab_status for update to anon using (true);
create policy "anon can delete vocab_status"
  on vocab_status for delete to anon using (true);
