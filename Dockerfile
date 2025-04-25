FROM python:3.9-slim
LABEL authors="yousef"

#ENTRYPOINT ["top", "-b"]


RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

Copy . .
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]