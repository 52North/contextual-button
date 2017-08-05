FROM python:latest

WORKDIR /app

COPY ./app /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]
