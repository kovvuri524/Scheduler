FROM python:3.12-slim

ENV TZ=Asia/Kolkata

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "scheduler.py"]