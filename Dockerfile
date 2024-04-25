FROM python:3.11

WORKDIR /app

COPY ./convert.py .

RUN apt-get update && apt-get install -y git

RUN pip install "huggingface_hub[cli]"

CMD ["python", "convert.py"]