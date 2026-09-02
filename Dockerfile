FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.docker.txt /app/requirements.docker.txt
RUN pip install --no-cache-dir -r requirements.docker.txt
COPY . /app
EXPOSE 8000
CMD ["gunicorn","--workers","3","--bind","0.0.0.0:8000","--access-logfile","-","chess_club.wsgi:application"]
