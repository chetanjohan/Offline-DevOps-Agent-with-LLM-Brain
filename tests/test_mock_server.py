import requests
import threading
import time
from src.llm.mock_server import run_server


def test_mock_server_basic():
    server, thread = run_server(port=8766, block=False)
    time.sleep(0.1)  # wait for server to start

    resp = requests.post('http://127.0.0.1:8766/generate', json={'prompt': 'Hello'})
    assert resp.status_code == 200
    data = resp.json()
    assert data['text'] == 'MOCKED: Hello'

    server.shutdown()
    thread.join(timeout=1)
