FROM python:3.9-slim

WORKDIR /app
COPY req.txt /app/req.txt
COPY ray-init-test.py /app/

RUN pip install --no-cache-dir -r req.txt

CMD ["python", "ray-init-test.py"]