// Language selector
const langSelect = document.getElementById('language-select');
if (langSelect) {
  const saved = localStorage.getItem('language') || 'en';
  langSelect.value = saved;
  langSelect.addEventListener('change', () => {
    localStorage.setItem('language', langSelect.value);
  });
}

function setupRecorder(buttonId, endpoint, resultId) {
  const btn = document.getElementById(buttonId);
  if (!btn) return;
  let mediaRecorder;
  let chunks = [];
  let stream;

  btn.addEventListener('click', async () => {
    if (!mediaRecorder || mediaRecorder.state === 'inactive') {
      chunks = [];
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = e => chunks.push(e.data);
      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        if (stream) stream.getTracks().forEach(t => t.stop());
        let data = {};
        try {
          const fd = new FormData();
          fd.append('audio', blob, 'recording.webm');
          fd.append('language', localStorage.getItem('language') || 'en');
          const resp = await fetch(endpoint, { method: 'POST', body: fd });
          data = await resp.json();
        } catch (err) {
          console.error('Upload failed', err);
          data = { message: 'Error processing recording' };
        } finally {
          btn.classList.remove('btn-danger');
          btn.textContent = btn.dataset.original;
        }
        const resultEl = document.getElementById(resultId);
        if (resultEl) resultEl.textContent = data.message || data.result || '';
        mediaRecorder = null;
      };
      mediaRecorder.start();
      btn.dataset.original = btn.textContent;
      btn.textContent = 'Recording... Press again to stop';
      btn.classList.add('btn-danger');
    } else {
      btn.classList.remove('btn-danger');
      btn.textContent = btn.dataset.original;
      mediaRecorder.stop();
    }
  });
}

const recordResultId = document.getElementById('record-result') ? 'record-result' : 'result';
const queryResultId = document.getElementById('query-result') ? 'query-result' : 'result';
setupRecorder('record-btn', '/record', recordResultId);
setupRecorder('query-btn', '/query', queryResultId);

// Fallback typed query form
const queryForm = document.getElementById('query-form');
if (queryForm) {
  queryForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = document.getElementById('query').value;
    const resp = await fetch('/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    const data = await resp.json();
    const resultEl = document.getElementById('query-result') || document.getElementById('result');
    if (resultEl) resultEl.textContent = data.result;
  });
}
