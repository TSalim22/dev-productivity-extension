# Dev Productivity Extension

A browser focus timer with a local Python statistics service.

This is a small, independent Python portfolio project. The code favours ordinary functions and clear modules over complex architecture.

## Setup

Requires Python 3.12+ (desktop tools also require Tkinter, included with the standard Windows Python installer).

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux instead: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python app.py
```

Run commands from this repository's root. Web apps bind to localhost by default. Each app is independent, so stop one before starting another on the same port.

## Check it

```sh
python -m pytest -q
```

## Dates

The commit author dates have been deliberately arranged between October 2025 and October 2026 at the portfolio owner's request. They are presentation metadata, not a record of the actual development timeline. Repository creation and upload timestamps remain the real dates.

## Load the extension

1. Start `python app.py` and keep it running. It prints a random local service key.
2. In Chrome or Edge, open the extensions page (`chrome://extensions` or `edge://extensions`), enable Developer mode and choose **Load unpacked**.
3. Select the repository's `extension` folder. Open a normal website, then open the extension popup.
4. Paste the key printed by Python, select the duration and start. The alarm continues while the popup is closed.
5. Completed sessions are saved to http://127.0.0.1:5050. If the service is offline, the extension retries in a minute. Cancel discards the active session.

The Python service uses SQLite and requires the local key for writes. The extension stores domain names and minutes only, not full URLs or page content. Keep the service local. Its extension folder necessarily uses JavaScript because browser extensions cannot run Python or Java directly. The focus timer records a planned session on completion; it does not measure attention or track tab switching. Extension storage is local but is not an encrypted secret store.

Backend behaviour has automated tests. Unpacked extension loading and alarm behaviour require a manual Chrome/Edge check; JavaScript syntax is checked separately.

## Optional local container

```sh
docker build -t dev-productivity-extension .
docker run --rm -p 127.0.0.1:5050:5050 dev-productivity-extension
```

This runs a local demonstration server. Container storage is temporary unless you mount a volume for `instance/`. Docker commands were supplied but Docker is not installed in the development environment, so container execution was not verified here.
