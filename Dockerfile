FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONDONTWRITEBYTECODE=1 DATA_DIR=/data
EXPOSE 8000
CMD ["python", "-m", "app.main"]
