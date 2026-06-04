FROM python:3.12-slim

RUN pip install uv
RUN uv pip install --system browser-use
RUN uvx browser-use install

WORKDIR /app
COPY find_and_login.py .

CMD ["python", "-u", "find_and_login.py"]
