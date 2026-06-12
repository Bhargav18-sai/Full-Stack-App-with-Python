// ── Inline Edit Logic ─────────────────────────────────────────

document.querySelectorAll('.edit-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const id   = btn.dataset.id;
    const span = document.querySelector(`.task-text[data-id="${id}"]`);

    // ── Enter edit mode ──
    if (span.contentEditable !== 'true') {
      span.contentEditable = 'true';
      span.focus();

      // move cursor to end
      const range = document.createRange();
      const sel   = window.getSelection();
      range.selectNodeContents(span);
      range.collapse(false);
      sel.removeAllRanges();
      sel.addRange(range);

      btn.textContent = '💾';  // change icon to Save
      btn.title = 'Save changes';

    // ── Save edit ──
    } else {
      saveEdit(id, span, btn);
    }
  });
});

// Save on Enter key, cancel on Escape
document.querySelectorAll('.task-text').forEach(span => {
  span.addEventListener('keydown', e => {
    const id  = span.dataset.id;
    const btn = document.querySelector(`.edit-btn[data-id="${id}"]`);

    if (e.key === 'Enter') {
      e.preventDefault();
      saveEdit(id, span, btn);
    }
    if (e.key === 'Escape') {
      span.contentEditable = 'false';
      btn.textContent = '✏️';
      location.reload();   // reload to restore original text
    }
  });
});

async function saveEdit(id, span, btn) {
  const newTask = span.textContent.trim();
  if (!newTask) { alert('Task cannot be empty!'); return; }

  try {
    const res  = await fetch(`/edit/${id}`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ task: newTask })
    });
    const data = await res.json();

    if (data.success) {
      span.textContent   = data.task;
      span.contentEditable = 'false';
      btn.textContent    = '✏️';
      btn.title          = 'Edit task';
    } else {
      alert('Could not save — please try again.');
    }
  } catch (err) {
    console.error(err);
    alert('Network error.');
  }
}
