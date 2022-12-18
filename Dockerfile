FROM python:3.10-slim

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY core core
COPY goals goals
COPY todolist todolist
COPY manage.py .
#COPY README.md .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
