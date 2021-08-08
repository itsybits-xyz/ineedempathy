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

`/etc/nginx/sites-available/ineedempathy`
~~~
server {
        listen 80;
        listen [::]:80;
        server_name ineedempathy.com;

        location / {
                include proxy_params;
                proxy_pass http://127.0.0.1:8000;
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
sudo update-alternatives --config editor
sudo visudo


# add to the bottom:
# enable sudo w/o password
baylee ALL=(ALL) NOPASSWD: ALL
amjith ALL=(ALL) NOPASSWD: ALL
```
