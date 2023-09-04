FROM ubuntu:22.04
MAINTAINER Alain Homewood
LABEL version="0.1-alpha1"

# Copy Sushi Train
COPY . /opt/sushitrain/

# Install Python3
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget

# Install Python packages
RUN pip3 install -r /opt/sushitrain/requirements.txt

# Fetch Maxmind databases
RUN wget "https://github.com/inzlain/GeoLite.mmdb/raw/download/GeoLite2-Country.mmdb" -O /opt/sushitrain/thirdparty/maxmind/GeoLite2-Country.mmdb && \
    wget "https://github.com/inzlain/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb" -O /opt/sushitrain/thirdparty/maxmind/GeoLite2-ASN.mmdb

# Run Sanic
ENV PYTHONUNBUFFERED=1
RUN chmod +x "/opt/sushitrain/entrypoint.sh"
CMD ["/opt/sushitrain/entrypoint.sh"]