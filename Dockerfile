FROM python:3.13.3-slim
WORKDIR /app

COPY . /app

CMD ["python", "HomePage.py"]