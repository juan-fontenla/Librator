ARG SPIDER

FROM python:3.9.12

WORKDIR /usr/share/scrapper

RUN pip3 install scrapy
RUN pip3 install scrapy_splash
RUN pip3 install elasticsearch

COPY . .

ARG SPIDER
ENV SPIDER=${SPIDER}

CMD scrapy crawl ${SPIDER}