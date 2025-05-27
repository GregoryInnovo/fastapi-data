FROM python:3.12-bullseye

WORKDIR /app

COPY ./app ./app
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]