import json

from starlette.testclient import TestClient

from .main import app, db

client = TestClient(app, base_url='http://127.0.0.1:8080')

def test_get_accept_to_unsupported_url():
    response = client.get("/")
    good_data = {
        "status": "Not Found"
    }
    assert response.json() == good_data

def test_add_links():
    db.delete('linkHistory:domains')

    input_data = {
        "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru", "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
        ]
    }
    response = client.post("/visited_links", data=json.dumps(input_data))
    good_data = {"status": "ok"}

    assert response.json() == good_data

def test_add_links_without_data():
    db.delete('linkHistory:domains')
    input_data = {}
    response = client.post("/visited_links", data=json.dumps(input_data))
    good_data = {"status": "Массив ссылок отсутствует..."}

    assert response.json() == good_data

def test_get_domains_with_correct_data():
    db.delete('linkHistory:domains')
    input_data = {
        "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
        ]
    }
    client.post("/visited_links", data=json.dumps(input_data))

    response = client.get("/visited_domains?from=1&to=100000000000")
    good_data = {
        "domains": [
            "funbox.ru",
            "stackoverflow.com",
            "ya.ru"
        ],
        "status": "ok"
    }

    assert response.json() == good_data

def test_get_domains_without_parameters():
    db.delete('linkHistory:domains')
    input_data = {
        "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru", "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
        ]
    }
    client.post("/visited_links", data=json.dumps(input_data))

    response = client.get("/visited_domains")
    good_data = {'status': [{'loc': ['query', 'from'], 'msg': 'field required', 'type': 'value_error.missing'},
                            {'loc': ['query', 'to'], 'msg': 'field required', 'type': 'value_error.missing'}]}

    assert response.json() == good_data

def test_get_domains_with_incorrect_parameters():
    # when date_start(from) > date_end(to)
    db.delete('linkHistory:domains')
    input_data = {
        "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru", "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
        ]
    }
    client.post("/visited_links", data=json.dumps(input_data))

    response = client.get("/visited_domains?from=10&to=1")
    good_data = {
        "domains": [],
        "status": "Некорректный интервал времени"
    }
    assert response.json() == good_data

def test_get_domains_when_db_empty():
    db.delete('linkHistory:domains')

    response = client.get("/visited_domains?from=1&to=10")
    good_data = {
        "domains": [],
        "status": "ok"
    }
    assert response.json() == good_data