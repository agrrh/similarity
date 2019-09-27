FROM python:3-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./ ./

RUN mkdir /code

ENV SIMILARITY_CODE_DIR /code

CMD ["python3", "main.py", "${SIMILARITY_CODE_DIR}"]
