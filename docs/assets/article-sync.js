// 기사 보관(🔖)과 메모(📝)를 Supabase에 저장 · 동기화
(function () {
  const sb = window.supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);

  let saved = {};        // { article_url: { bookmarked: bool, memo: string, title: string, updated_at: string } }
  let onChange = function () {};

  async function load() {
    const { data, error } = await sb.from('saved_articles')
      .select('article_url, title, bookmarked, memo, updated_at')
      .order('updated_at', { ascending: false });
    if (!error && data) {
      saved = {};
      data.forEach(r => { saved[r.article_url] = { bookmarked: !!r.bookmarked, memo: r.memo || '', title: r.title || '', updated_at: r.updated_at }; });
    }
    onChange();
  }

  async function persist(url) {
    const s = saved[url];
    await sb.from('saved_articles').upsert(
      { article_url: url, title: s.title, bookmarked: s.bookmarked, memo: s.memo, updated_at: new Date().toISOString() },
      { onConflict: 'article_url' }
    );
  }

  function entryOf(url, title) {
    if (!saved[url]) saved[url] = { bookmarked: false, memo: '', title: title || '' };
    if (title && !saved[url].title) saved[url].title = title;
    return saved[url];
  }

  function toggleBookmark(url, title) {
    const s = entryOf(url, title);
    s.bookmarked = !s.bookmarked;
    onChange();
    persist(url);
  }

  function setMemo(url, title, memo) {
    const s = entryOf(url, title);
    s.memo = memo;
    persist(url);
  }

  function getBookmarked() {
    return Object.entries(saved)
      .filter(([, s]) => s.bookmarked)
      .map(([url, s]) => ({ url, title: s.title, memo: s.memo, updated_at: s.updated_at }));
  }

  window.articleSync = {
    of: (url) => saved[url] || { bookmarked: false, memo: '', title: '' },
    onChange: (fn) => { onChange = fn; load(); },
    toggleBookmark,
    setMemo,
    getBookmarked,
  };
})();
