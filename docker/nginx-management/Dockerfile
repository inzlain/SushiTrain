FROM ubuntu:22.04
MAINTAINER Alain Homewood
LABEL version="0.1-alpha1"

# Install NGINX Extras
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y nginx-extras openssl curl sed

# Copy configuration
COPY management.conf /etc/nginx/sites-available/default

# Configure SSL/TLS
RUN mkdir -p "/etc/nginx/ssl/"
RUN curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "/etc/nginx/ssl/options-ssl-nginx.conf"
RUN curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "/etc/nginx/ssl/ssl-dhparams.pem"

# Run NGINX
COPY ./entrypoint.sh /opt/nginx/entrypoint.sh
RUN chmod +x "/opt/nginx/entrypoint.sh"
CMD ["/opt/nginx/entrypoint.sh"]