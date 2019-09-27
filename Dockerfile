FROM python:3-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./ ./

RUN chmod +x /app/main.py \
  && ln -s /app/main.py /usr/local/bin/similarity

RUN mkdir /code

ENV SIMILARITY_CODE_DIR /code

ENTRYPOINT ["similarity"]
CMD ["${SIMILARITY_CODE_DIR}"]
