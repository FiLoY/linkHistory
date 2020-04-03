FROM python:3.7.7-slim

WORKDIR /app

EXPOSE 8080

ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD . /app/

ENV DB_HOST=redis

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]