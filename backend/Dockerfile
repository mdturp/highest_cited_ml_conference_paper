# Fast API Backend
FROM python:3.10-slim-buster

# Copy requirements.txt
COPY requirements.txt ./requirements.txt

# Install requirements
RUN pip install -r requirements.txt

# Copy source code
COPY ./src ./src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
