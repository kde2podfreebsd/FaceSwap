FROM python:3.11

WORKDIR /app

COPY . /app

RUN python -m venv /venv

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

RUN /venv/bin/python -m pip install --upgrade pip
RUN /venv/bin/python -m pip install -r requirements.txt

ENV PYTHONPATH=/app

CMD ["/venv/bin/python", "Telegram/main.py"]
