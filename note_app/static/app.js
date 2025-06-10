// Recording functionality
const recordBtn = document.getElementById('record-btn');
if (recordBtn) {
  let mediaRecorder;
  let chunks = [];
  recordBtn.addEventListener('click', async () => {
    if (!mediaRecorder || mediaRecorder.state === 'inactive') {
      chunks = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = e => chunks.push(e.data);
      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        document.getElementById('status').textContent = 'Transcribing...';
        const fd = new FormData();
        fd.append('audio', blob, 'recording.webm');
        const resp = await fetch('/record', { method: 'POST', body: fd });
        const data = await resp.json();
        document.getElementById('status').textContent = '';
        document.getElementById('result').textContent = data.message;
      };
      mediaRecorder.start();
      recordBtn.textContent = 'Stop Recording';
    } else {
      mediaRecorder.stop();
      recordBtn.textContent = 'Start Recording';
    }
  });
}

// Query functionality
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
    document.getElementById('query-result').textContent = data.result;
  });
}
