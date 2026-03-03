# Dev Productivity Extension

A browser focus timer with a Python app that saves your sessions.

## Run it

Python 3.12 or later. Run these commands from the project folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python app.py
```

On macOS or Linux, activate with `source .venv/bin/activate` instead.

## How to use it

1. Keep the Python app running and copy the key it prints.
2. Open `chrome://extensions` or `edge://extensions` and turn on Developer mode.
3. Choose **Load unpacked** and select the `extension` folder.
4. Open a website, click the extension, paste the key and start a timer.
5. View your sessions at http://127.0.0.1:5050.

The timer keeps running when the popup closes. Cancel it before starting another one. Failed saves are retried without counting the same session twice.

The app stores the domain and minutes locally. The timer records planned focus time; it doesn't track your activity. Browser alarm behaviour still needs a manual Chrome or Edge check.

## Tests

```sh
python -m pytest -q
```

## Docker (optional)

```sh
docker build -t dev-productivity-extension .
docker run --rm -p 127.0.0.1:5050:5050 dev-productivity-extension
```

Use a volume for saved data. Docker hasn't been tested locally.
