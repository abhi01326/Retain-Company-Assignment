import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_shorten_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "not-a-url"})
    assert response.status_code == 400

def test_shorten_and_redirect(client):
    res = client.post('/api/shorten', json={"url": "https://example.com"})
    data = res.get_json()
    assert 'short_code' in data
    code = data['short_code']

    res2 = client.get(f'/{code}', follow_redirects=False)
    assert res2.status_code == 302

def test_stats(client):
    res = client.post('/api/shorten', json={"url": "https://example.com"})
    code = res.get_json()['short_code']
    for _ in range(3):
        client.get(f'/{code}')
    res2 = client.get(f'/api/stats/{code}')
    stats = res2.get_json()
    assert stats['clicks'] == 3
    assert stats['url'] == "https://example.com"
