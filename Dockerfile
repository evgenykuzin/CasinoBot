FROM python:3.8-slim-buster

WORKDIR /app

#ENV PYTHONPATH = /workspace

COPY requirements.txt requirements.txt

RUN  python -m pip install --upgrade pip
RUN  python -m pip install -r requirements.txt
RUN  python -m pip install pyTelegramBotAPI

COPY Jopsbank .

CMD [ "python", "main.py" ]