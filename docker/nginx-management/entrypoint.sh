#!/bin/bash

if [ ! -s "/etc/letsencrypt/live/$MANAGEMENT_HOSTNAME/fullchain.pem" ]
then
    mkdir -p "/etc/letsencrypt/live/$MANAGEMENT_HOSTNAME/"
    openssl req -x509 -nodes -newkey rsa:4096 -days 365 -keyout "/etc/letsencrypt/live/$MANAGEMENT_HOSTNAME/privkey.pem" -out "/etc/letsencrypt/live/$MANAGEMENT_HOSTNAME/fullchain.pem" -subj "/CN=sushi-management"
fi

sed -i "s/\$MANAGEMENT_HOSTNAME/$MANAGEMENT_HOSTNAME/g" /etc/nginx/sites-available/default

while :; do sleep 6h; nginx -s reload; done & exec nginx -g "daemon off;"