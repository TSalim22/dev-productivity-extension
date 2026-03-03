chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name !== 'focus') return;
  const {session, key} = await chrome.storage.local.get(['session', 'key']);
  if (!session) return;
  try {
    const response = await fetch('http://127.0.0.1:5050/api/sessions', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-Focus-Key': key},
      body: JSON.stringify({session_id: session.id, domain: session.domain, minutes: session.minutes})
    });
    if (!response.ok) throw new Error('Save failed');
    const current = await chrome.storage.local.get('session');
    if (current.session?.id !== session.id) return;
    await chrome.storage.local.remove('session');
    await chrome.storage.local.set({lastMessage: 'Session complete and saved!'});
    await chrome.action.setBadgeText({text: '✓'});
  } catch {
    const current = await chrome.storage.local.get('session');
    if (current.session?.id !== session.id) return;
    // Keep the completed session and retry when the local service returns.
    await chrome.storage.local.set({lastMessage: 'Service unavailable; retrying in one minute.'});
    await chrome.alarms.create('focus', {delayInMinutes: 1});
  }
});
