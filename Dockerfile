FROM python:3.12-slim

# Installa uv e browser-use
RUN pip install uv
RUN uv pip install --system browser-use
RUN uvx browser-use install

WORKDIR /app

# Copia lo script
COPY find_and_login.py .
COPY requirements.txt .

# Installa dipendenze aggiuntive (se necessarie)
RUN pip install --no-cache-dir -r requirements.txt

# Comando di avvio
CMD ["python", "-u", "find_and_login.py"]