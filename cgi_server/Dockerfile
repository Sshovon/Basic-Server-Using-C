FROM httpd:alpine

RUN mkdir -p /usr/local/apache2/DB && \
    chmod -R 777 /usr/local/apache2/DB

RUN apk update && \
    apk add sqlite bash xmlstarlet

COPY DB/* /usr/local/apache2/DB/
COPY cgi/* /usr/local/apache2/cgi-bin/
COPY httpd.conf /usr/local/apache2/conf/httpd.conf

RUN /usr/local/apache2/DB/db.sh

EXPOSE 80
