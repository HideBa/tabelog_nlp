# sushi_dockerディレクトリの作成

```
mkdir sushi_docker
```

この中にDockerfileとuser_dic.csvとdjangoのアプリのディレクトリを入れる

```
cd sushi_docker
docker build -t container:8.4 .
docker run -itd -p 127.0.0.1:8000:8000 イメージのID
docker exec -it コンテナのID /bin/bash

/etc/init.d/postgresql start
postgres=# CREATE USER sushi_proj WITH PASSWORD 'sushi_proj_pass';
CREATE ROLE
postgres=# create database sushi_proj_db;
CREATE DATABASE
postgres=# GRANT CONNECT ON DATABASE sushi_proj_db TO sushi_proj;
GRANT
postgres=# GRANT ALL PRIVILEGES ON DATABASE sushi_proj_db TO sushi_proj;
GRANT
postgres=# GRANT ALL on all tables in schema public to sushi_proj;
GRANT
postgres=# \q

/etc/mecabrcを開いてパスを通す
userdic = /usr/lib/mecab/dic/user.dicとする
```


## python activate
* `python3.6 manage.py runserver 0.0.0.0:8000`
