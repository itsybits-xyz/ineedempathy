# supervisord

```
sudo apt install supervisor
sudo service supervisor start
sudo service supervisor status

sudo supervisorctl   # Launch interactive supervisord controller
```

Edit:

`/etc/supervisor/supervisord.conf`

~~~
[include]
files = /var/www/ineedempathy/supervisord.conf
~~~


# Nginx

`systemctl edit --full nginx.service`

Change 1048576 to `ulimit -Hn`

~~~
[Service]
LimitNOFILE=1048576
~~~

`/etc/nginx/nginx.conf`

Change 1024 to `ulimit -n`
Change 1048576 to `ulimit -Hn`

~~~
worker_rlimit_nofile 1048576;

events {
    worker_connections 1024;
}
~~~

`/etc/nginx/sites-available/ineedempathy`
~~~
upstream empathyserver {
    hash $request_uri;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
    server 127.0.0.1:8004;
}
server {
        listen 80;
        listen [::]:80;
        server_name ineedempathy.com;

        location / {
                include proxy_params;
                proxy_pass http://empathyserver;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "Upgrade";
        }

        location ~ \.(ico|png|json|txt) {
                index /var/www/ineedempathy/templates;
                root /var/www/ineedempathy/templates;
        }
}
~~~

``` bash
ln -s /etc/nginx/sites-available/ineedempathy /etc/nginx/sites-enabled/ineedempathy
```

# Python

Install from source:

```
sudo apt install wget build-essential checkinstall 
sudo apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev 
cd /opt
sudo wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
tar xzf Python-3.9.6.tgz
cd Python-3.9.6
sudo ./configure --enable-optimizations 
sudo make altinstall
python3.9 -V
sudo ln -s /usr/local/bin/pip3.9 /usr/bin/pip
sudo ln -s /usr/local/bin/python3.9 /usr/bin/python
python -V
```


# Project Files

```
cd /var/www
mkdir ineedempathy
chown root:www-data /var/www/ineedempathy
chmod 775 /var/www/ineedempathy
```

# Server Users

Enable no sudo for our users

```
# add users
sudo adduser amjith
sudo adduser baylee
sudo adduser web-runner

ln -s /var/www/ineedempathy ~/ineedempathy

# add group
groupadd -g 10000 webteam
sudo groupadd -g 10000 root
sudo groupadd -g 10000 amjith
sudo groupadd -g 10000 baylee
sudo groupadd -g 10000 web-runner

# don't require passwords on sudo
sudo update-alternatives --config editor
sudo visudo

baylee ALL=(ALL) NOPASSWD: ALL
amjith ALL=(ALL) NOPASSWD: ALL
web-runner ALL=(ALL) NOPASSWD: ALL
```
