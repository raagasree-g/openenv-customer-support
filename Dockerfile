FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install pydantic

RUN pip install --no-cache-dir pydantic

CMD ["python", "inference.py"]