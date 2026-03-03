import os
import secrets
import sqlite3
import uuid
from pathlib import Path
from flask import Flask, request, jsonify, render_template


def create_app(config=None):
    app = Flask(__name__)
    folder = Path(app.instance_path)
    folder.mkdir(exist_ok=True)
    key_path = folder / 'extension.key'
    if not key_path.exists():
        key_path.write_text(secrets.token_urlsafe(32))
    app.config.update(APP_TITLE='Focus Sessions', APP_DESCRIPTION='Local focus statistics from your browser timer.',
        DATABASE=str(folder/'focus.db'), EXTENSION_KEY=os.getenv('EXTENSION_KEY') or key_path.read_text(), MAX_CONTENT_LENGTH=8192)
    if config:
        app.config.update(config)

    def connect():
        connection = sqlite3.connect(app.config['DATABASE'])
        connection.row_factory = sqlite3.Row
        return connection

    with connect() as connection:
        connection.execute('CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, domain TEXT NOT NULL, minutes INTEGER NOT NULL, created TEXT DEFAULT CURRENT_TIMESTAMP)')
        columns = {row[1] for row in connection.execute('PRAGMA table_info(sessions)')}
        if 'session_id' not in columns:
            connection.execute('ALTER TABLE sessions ADD COLUMN session_id TEXT')
        connection.execute('CREATE UNIQUE INDEX IF NOT EXISTS session_identity ON sessions(session_id)')

    @app.get('/')
    def index():
        with connect() as connection:
            items = connection.execute('SELECT domain, SUM(minutes) AS minutes, COUNT(*) AS count FROM sessions GROUP BY domain ORDER BY minutes DESC').fetchall()
        return render_template('index.html', title='Focus dashboard', items=items)

    @app.post('/api/sessions')
    def save():
        if not secrets.compare_digest(request.headers.get('X-Focus-Key',''), app.config['EXTENSION_KEY']):
            return jsonify(error='Invalid local service key.'), 401
        data = request.get_json(silent=True) or {}
        domain, minutes = data.get('domain'), data.get('minutes')
        session_id = data.get('session_id')
        if not isinstance(domain,str) or not domain or len(domain)>253 or type(minutes) is not int or not 1<=minutes<=180:
            return jsonify(error='Invalid session.'), 400
        try:
            if not isinstance(session_id,str) or str(uuid.UUID(session_id)) != session_id:
                raise ValueError()
        except ValueError:
            return jsonify(error='Invalid session identity.'), 400
        with connect() as connection:
            connection.execute('INSERT OR IGNORE INTO sessions (session_id,domain,minutes) VALUES (?,?,?)', (session_id,domain,minutes))
        return jsonify(saved=True), 201

    return app


if __name__ == '__main__':
    application = create_app()
    print('Paste this local service key into the extension settings:')
    print(application.config['EXTENSION_KEY'])
    application.run(host=os.getenv('HOST','127.0.0.1'), port=5050)
