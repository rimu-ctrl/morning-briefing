// 단어장 별표(★)/암기완료(●) 상태를 Supabase에 저장 · 동기화
// 별표와 암기완료는 서로 독립적으로 켤 수 있음 (둘 다 가능)
(function () {
  const sb = window.supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);

  let status = {};       // { word_id: { starred: bool, learned: bool } }
  let onChange = function () {};

  function wordIdOf(word) {
    return word.replace(/ /g, '_').replace(/\//g, '_');
  }

  async function load() {
    const { data, error } = await sb.from('vocab_status').select('word_id, starred, learned');
    if (!error && data) {
      status = {};
      data.forEach(r => { status[r.word_id] = { starred: !!r.starred, learned: !!r.learned }; });
    }
    onChange();
  }

  async function persist(wid) {
    const st = status[wid];
    await sb.from('vocab_status').upsert(
      { word_id: wid, starred: st.starred, learned: st.learned, updated_at: new Date().toISOString() },
      { onConflict: 'word_id' }
    );
  }

  function toggle(wid, field) {
    const cur = status[wid] || { starred: false, learned: false };
    cur[field] = !cur[field];
    status[wid] = cur;
    onChange();
    persist(wid);
  }

  window.vocabSync = {
    wordIdOf,
    statusOf: (wid) => status[wid] || { starred: false, learned: false },
    onChange: (fn) => { onChange = fn; load(); },
  };
  window.toggleStar = (wid) => toggle(wid, 'starred');
  window.toggleCheck = (wid) => toggle(wid, 'learned');
})();
