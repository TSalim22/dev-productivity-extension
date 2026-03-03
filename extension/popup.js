const status = document.getElementById('status');
async function refresh() {
  const data = await chrome.storage.local.get(['session', 'key', 'lastMessage']);
  document.getElementById('key').value = data.key || '';
  status.textContent = data.session ? `Focusing on ${data.session.domain} until ${new Date(data.session.end).toLocaleTimeString()}` : (data.lastMessage || 'Ready for a focused session.');
}
document.getElementById('start').addEventListener('click', async () => {
  const active = await chrome.storage.local.get('session');
  if (active.session) { status.textContent = 'Cancel the current session before starting another.'; return; }
  const minutes = Number(document.getElementById('minutes').value);
  const key = document.getElementById('key').value.trim();
  if (!Number.isInteger(minutes) || minutes < 1 || minutes > 180 || !key) {
    status.textContent = 'Enter 1–180 minutes and the key printed by Python.';
    return;
  }
  const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
  try {
    const url = new URL(tab.url);
    if (!['http:', 'https:'].includes(url.protocol)) throw new Error('Unsupported page');
    const end = Date.now() + minutes * 60000;
    await chrome.storage.local.set({key, session: {id: crypto.randomUUID(), domain: url.hostname, minutes, end}, lastMessage: ''});
    await chrome.alarms.create('focus', {when: end});
    refresh();
  } catch {
    status.textContent = 'Open a normal website before starting a session.';
  }
});
document.getElementById('cancel').addEventListener('click', async () => {
  await chrome.alarms.clear('focus');
  await chrome.storage.local.remove('session');
  await chrome.storage.local.set({lastMessage: 'Session cancelled.'});
  refresh();
});
refresh();
