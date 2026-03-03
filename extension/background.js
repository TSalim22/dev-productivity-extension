chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name !== 'focus') return;
  const {session, key} = await chrome.storage.local.get(['session', 'key']);
  if (!session) return;
  try {
    const response = await fetch('http://127.0.0.1:5050/api/sessions', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-Focus-Key': key},
      body: JSON.stringify({domain: session.domain, minutes: session.minutes})
    });
    if (!response.ok) throw new Error('Save failed');
    await chrome.storage.local.remove('session');
    await chrome.storage.local.set({lastMessage: 'Session complete and saved!'});
    await chrome.action.setBadgeText({text: '✓'});
  } catch {
    // Keep the completed session and retry when the local service returns.
    await chrome.storage.local.set({lastMessage: 'Service unavailable; retrying in one minute.'});
    await chrome.alarms.create('focus', {delayInMinutes: 1});
  }
});
