## Description
Web-приложение для простого учета посещенных ссылок.

## Technical specifications
 - python 3.7.7;
 - fastAPI 0.53.2.

## Getting started
 - `git clone https://github.com/FiLoY/linkHistory.git` 
 - `cd linkHistory`
 - `docker-compose up`
 
## Examples
Добавление ссылок: 
  - `curl -X POST "http://127.0.0.1:8080/visited_links" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"links\":[\"https://ya.ru\",\"https://ya.ru?q=123\",\"funbox.ru\",\"https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor\"]}`
  
Получения списка доменов за интервал времени от 1 до 100000000000: 
 - `curl -X GET "http://127.0.0.1:8080/visited_domains?from=1&to=100000000000" -H "accept: application/json"` 

## Tests
Для тестирования использовался pytest:
 - `pytest test_mail.py`
