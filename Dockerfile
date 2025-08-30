FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential python3-dev libopenblas-dev liblapack-dev gfortran git \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8888

CMD ["sh", "-c", "panel serve app.py --address=0.0.0.0 --port=${PORT:-8888} --allow-websocket-origin='*' --prefix='' --index='app'"]
