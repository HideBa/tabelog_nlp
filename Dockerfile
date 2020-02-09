#ベースイメージ
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get update \
    && apt-get install -y mecab \
    && apt-get install -y libmecab-dev \
    && apt-get install -y mecab-ipadic-utf8\
    && apt-get install -y git\
    && apt-get install -y make\
    && apt-get install -y curl\
    && apt-get install -y xz-utils\
    && apt-get install -y file\
    && apt-get install -y sudo\
    && apt-get install -y wget

RUN apt-get install -y python-psycopg2

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git\
    && cd mecab-ipadic-neologd\
    && bin/install-mecab-ipadic-neologd -n -y

RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN python3.6 -m pip install pip --upgrade

RUN pip install numpy
RUN pip install pandas
RUN pip install sklearn
RUN pip install gensim
RUN pip install mecab-python3
RUN pip install django

WORKDIR /home
RUN mkdir foo
RUN mkdir foo/bar
COPY user_dic.csv foo/bar/user_dic.csv

WORKDIR /home/foo/bar
RUN /usr/lib/mecab/mecab-dict-index -d /usr/lib/mecab/dic/mecab-ipadic-neologd/ \ 
-u /usr/lib/mecab/dic/user.dic -f utf-8 -t utf-8 user_dic.csv

WORKDIR /

RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main" > \
    /etc/apt/sources.list.d/pgdg.list'
RUN apt -y install wget ca-certificates
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \ 
    sudo apt-key add -
RUN apt update
RUN apt -y install postgresql-10
RUN systemctl enable postgresql

RUN mkdir /app
COPY sushi_proj /app/sushi_proj

RUN pip install django-mathfilters
RUN pip install django-bootstrap4

RUN apt-get install libpq-dev
RUN pip install psycopg2