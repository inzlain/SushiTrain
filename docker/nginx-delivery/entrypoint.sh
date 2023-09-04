#!/bin/bash

if [ ! -s "/etc/letsencrypt/live/$DELIVERY_HOSTNAME/fullchain.pem" ]
then
    mkdir -p "/etc/letsencrypt/live/$DELIVERY_HOSTNAME/"
    openssl req -x509 -nodes -newkey rsa:4096 -days 365 -keyout "/etc/letsencrypt/live/$DELIVERY_HOSTNAME/privkey.pem" -out "/etc/letsencrypt/live/$DELIVERY_HOSTNAME/fullchain.pem" -subj "/CN=sushi-delivery"
fi

sed -i "s/\$DELIVERY_HOSTNAME/$DELIVERY_HOSTNAME/g" /etc/nginx/sites-available/default
sed -i "s:\$DELIVERY_PATH:$DELIVERY_PATH:g" /etc/nginx/sites-available/default

while :; do sleep 6h; nginx -s reload; done & exec nginx -g "daemon off;"