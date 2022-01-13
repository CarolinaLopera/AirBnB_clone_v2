#!/usr/bin/env bash
# Script to set up your web servers for the deployment of web_static.

if [ ! -d /etc/nginx ]
then
    apt-get -y update
    apt-get -y install nginx
fi

if [ ! -d /data/ ]
then
    mkdir -p /data/web_static/shared/
    mkdir -p /data/web_static/releases/test/
    echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
fi

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

echo "server {
       listen 80;
       listen [::]:80;

       root /var/www/html;
       index index.html;

       location /hbnb_static {
           alias /data/web_static/current/;
           index index.html;
       }

       location /redirect_me {
           rewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;
       }

       error_page 404 /404.html;
}" > /etc/nginx/sites-enabled/default
