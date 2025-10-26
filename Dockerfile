FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["fastapi", "run"]

FROM prom/prometheus
ADD prometheus.yml /etc/prometheus/