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
