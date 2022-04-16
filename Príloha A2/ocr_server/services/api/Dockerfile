FROM python:3.8.1-slim-buster

RUN apt-get update && apt-get install wget build-essential cmake libfreetype6-dev pkg-config libfontconfig-dev libjpeg-dev libopenjp2-7-dev -y
RUN wget https://poppler.freedesktop.org/poppler-data-0.4.9.tar.gz \
    && tar -xf poppler-data-0.4.9.tar.gz \
    && cd poppler-data-0.4.9 \
    && make install \
    && cd .. \
    && wget https://poppler.freedesktop.org/poppler-20.08.0.tar.xz \
    && tar -xf poppler-20.08.0.tar.xz \
    && cd poppler-20.08.0 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && ldconfig
CMD tail -f /dev/null

ENV WORKDIR=/usr/src/app
ENV USER=app
ENV APP_HOME=/home/app/web
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY ./text-sumarization-345613-9b9ab179b0d7.json $WORKDIR/gvision_key_api.json
ENV GOOGLE_APPLICATION_CREDENTIALS=$WORKDIR/gvision_key_api.json

WORKDIR $WORKDIR

RUN pip install --upgrade pip
COPY ./requirements.txt $WORKDIR/requirements.txt
RUN pip install -r requirements.txt


RUN adduser --system --group $USER
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY . $APP_HOME
RUN chown -R $USER:$USER $APP_HOME
USER $USER
