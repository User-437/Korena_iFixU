FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements-server.txt ./
RUN pip install --no-cache-dir -r requirements-server.txt
COPY app.py database.py models.py audit.py accounting.py seed.py manage.py server.py ./
COPY templates/ templates/
COPY static/ static/
RUN useradd --create-home korena
USER korena
EXPOSE 8000
# Initialize ONCE before starting workers; worker imports do not race to create tables.
CMD ["sh", "-c", "python manage.py init-db && exec gunicorn --bind 0.0.0.0:8000 --workers 2 --threads 4 --access-logfile - server:app"]
