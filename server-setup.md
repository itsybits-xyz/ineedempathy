```
sudo apt-get update
```

# supervisord

```
sudo apt install nginx -y
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

```
sudo apt install supervisor
```

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

## Horizontal Scaling

Run nginx on the leader droplet. Proxy the incoming requests to multiple follower droplets using the hashing. 

```
upstream empathyserver {
    hash $request_uri;
    server droplet1:8000;
    server droplet1:8001;
    server droplet2:8000;
    server droplet2:8001;
    server droplet3:8000;
    server droplet3:8001;
}
```

In the future we might look into the digitalocean load balancer instead of using nginx. 

## Scaling Nginx

### Single Core Limits

We usually can handle around ~500 connections. That's around ~100 rooms/~5
people per room.

### 4 Core Limits

If we go into Digital Ocean we can scale the application up, but it will shut
down the server, losing all current connections. If we scale this up to 4 core
(vs 1 we are at now) and change this nginx config, we can handle around ~2.6k
connections on the single droplet.

### Scaling Configuration

`systemctl edit --full nginx.service`

* Change 1048576 to `ulimit -Hn`

~~~
[Service]
LimitNOFILE=1048576
~~~

`/etc/nginx/nginx.conf`

* Change 1024 to `ulimit -n` * CORE_COUNT
* Change 1048576 to `ulimit -Hn`

~~~
worker_rlimit_nofile 1048576;

events {
    worker_connections 1024;
}
~~~

# Python

Install from source

```
sudo apt install wget build-essential checkinstall -y
sudo apt install libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev -y
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

# Server Users

Enable no sudo for our users

```
# add users
sudo adduser amjith
sudo adduser baylee
sudo adduser web-runner

ln -s /var/www/ineedempathy ~/ineedempathy
runuser -l amjith -c 'ln -s /var/www/ineedempathy ~/ineedempathy'
runuser -l baylee -c 'ln -s /var/www/ineedempathy ~/ineedempathy'
runuser -l web-runner -c 'ln -s /var/www/ineedempathy ~/ineedempathy'

# add group
groupadd -g 10000 webteam
usermod -a -G webteam root
usermod -a -G webteam amjith
usermod -a -G webteam baylee
usermod -a -G webteam web-runner

# don't require passwords on sudo
sudo update-alternatives --config editor
sudo visudo

baylee ALL=(ALL) NOPASSWD: ALL
amjith ALL=(ALL) NOPASSWD: ALL
web-runner ALL=(ALL) NOPASSWD: ALL
```

## Permissions

As root, ensure each user has the right authorized keys.

Repeat for every user `amjith`, `baylee` and `web-runner`.

```
cd /home/web-runner
mkdir -m 700 .ssh
chown web-runner:web-runner .ssh
cp ~/.ssh/authorized_keys ./.ssh
chown web-runner:web-runner ./.ssh/authorized_keys
```

# Project Files

```
cd /var/www
mkdir ineedempathy
chown root:webteam /var/www/ineedempathy
chmod 775 /var/www/ineedempathy
```
