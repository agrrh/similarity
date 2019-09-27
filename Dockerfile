FROM python:3-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./ ./

RUN mkdir /code

ENTRYPOINT python3 main.py
CMD /code
