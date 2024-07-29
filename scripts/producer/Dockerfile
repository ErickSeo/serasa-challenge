FROM python:3.9-slim

WORKDIR /app

# Copia os arquivos necessários
COPY requirements/requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . /app/

CMD ["python", "./src/__main__.py"]
