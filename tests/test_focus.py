from app import create_app


def test_sessions_require_key_and_appear_in_dashboard(tmp_path):
    client = create_app({'TESTING':True, 'DATABASE':str(tmp_path/'focus.db'), 'EXTENSION_KEY':'test-key'}).test_client()
    data = {'domain':'example.com','minutes':25}
    assert client.post('/api/sessions',json=data).status_code == 401
    assert client.post('/api/sessions',json=data,headers={'X-Focus-Key':'test-key'}).status_code == 201
    assert b'example.com' in client.get('/').data
    assert client.post('/api/sessions',json={**data,'minutes':True},headers={'X-Focus-Key':'test-key'}).status_code == 400
