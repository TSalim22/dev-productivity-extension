from app import create_app


def test_sessions_require_key_and_appear_in_dashboard(tmp_path):
    client = create_app({'TESTING':True, 'DATABASE':str(tmp_path/'focus.db'), 'EXTENSION_KEY':'test-key'}).test_client()
    data = {'session_id':'00000000-0000-4000-8000-000000000000','domain':'example.com','minutes':25}
    assert client.post('/api/sessions',json=data).status_code == 401
    assert client.post('/api/sessions',json=data,headers={'X-Focus-Key':'test-key'}).status_code == 201
    assert b'example.com' in client.get('/').data
    assert client.post('/api/sessions',json={**data,'minutes':True},headers={'X-Focus-Key':'test-key'}).status_code == 400


def test_retry_does_not_double_count(tmp_path):
    client = create_app({'TESTING':True,'DATABASE':str(tmp_path/'focus.db'),'EXTENSION_KEY':'test-key'}).test_client()
    data = {'session_id':'00000000-0000-4000-8000-000000000001','domain':'example.com','minutes':25}
    for _ in range(2):
        assert client.post('/api/sessions',json=data,headers={'X-Focus-Key':'test-key'}).status_code==201
    page = client.get('/').data
    assert b'<td>25</td>' in page and b'<td>1</td>' in page
    assert client.post('/api/sessions',json={**data,'session_id':'invalid'},headers={'X-Focus-Key':'test-key'}).status_code==400
