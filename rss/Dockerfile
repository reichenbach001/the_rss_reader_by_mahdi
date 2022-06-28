FROM python:3.9-slim-bullseye

WORKDIR /
COPY ./requirements.txt /requirements.txt
COPY ./rss_reader.py /rss_reader.py

RUN pip install -r requirements.txt

CMD [ "python", "rss_reader.py" ]