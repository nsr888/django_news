FROM alpine:latest

# Set environment variables.
# PYTHONDONTWRITEBYTECODE prevents Python from writing pyc files to disc.
# PYTHONUNBUFFERED Prevents Python from buffering stdout and stderr.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update 
RUN apk add bash \
	git \
	openssh \
	python3 \
	python3-dev \
	gcc \
	build-base \
	linux-headers \
	pcre-dev \
	postgresql-dev \
	musl-dev \
	libxml2-dev \
	libxslt-dev \
	nginx \
	curl \
	supervisor && \
	python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache

# install uwsgi now because it takes a little while
RUN pip3 install uwsgi

# setup all the configfiles
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

COPY ./requirements.txt /home/docker/code/news/

RUN apk add --no-cache --virtual .build-deps \
    gcc musl-dev python3-dev libffi-dev openssl-dev cargo && \
    pip3 install --no-cache-dir --ignore-installed six -r /home/docker/code/news/requirements.txt && \
    apk del .build-deps

# add (the rest of) our code
COPY . /home/docker/code/

WORKDIR /home/docker/
EXPOSE 8113
CMD ["supervisord", "-n", "-c", "/home/docker/code/supervisor-app.conf"]
