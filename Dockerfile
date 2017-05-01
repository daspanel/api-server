#FROM daspanel/python2.7-gunicorn
FROM daspanel/alpine-base
MAINTAINER Abner G Jacobsen <admin@daspanel.com>

# Parse arguments for the build command.
ARG VERSION
ARG VCS_URL
ARG VCS_REF
ARG BUILD_DATE

# A little bit of metadata management.
# See http://label-schema.org/  
LABEL org.label-schema.schema-version="1.0" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vendor="DASPANEL" \
      org.label-schema.version=$VERSION \
      org.label-schema.vcs-url=$VCS_URL \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.name="base-api" \
      org.label-schema.description="This service provides a Daspanel api server platform." \
      org.label-schema.architecture="x86_64" \
      org.label-schema.distribution="Alpine Linux" \
      org.label-schema.distribution-version="3.4" \
      info.daspanel.apiserver=$VERSION

ENV INSTALL_PATH /opt/daspanel/apps/apiserver
RUN mkdir -p $INSTALL_PATH

# Inject files in container file system
COPY container_data /
COPY api_server /opt/daspanel/apps/apiserver/api_server
COPY requirements /opt/daspanel/apps/apiserver/requirements

WORKDIR $INSTALL_PATH

RUN apk add --no-cache --update --virtual .build-deps \
        #build-base libffi-dev mariadb-dev python-dev libxml2-dev libxslt-dev \
        build-base bash gcc musl-dev git libressl-dev curl curl-dev python-dev libffi-dev \
        mariadb-dev python-dev libxml2-dev libxslt-dev \

    # Install python, pip
    && apk add --no-cache --update libssl1.0 libcurl python \
    && curl "https://bootstrap.pypa.io/get-pip.py" | python \

    # Install pyCurl
    && export PYCURL_SSL_LIBRARY=openssl \
    && pip install --compile pycurl==7.43.0 \

    # Install basic python packages used by Daspanel
    && pip install gunicorn==19.7.1 setproctitle gevent \

    # Install pip packages
    && pip install -r $INSTALL_PATH/requirements/dev.txt \

    # Cleanup
    && apk --purge -v del .build-deps \
    && rm -rf /var/cache/apk/* \
    && rm -rf /tmp/src \
    && rm -rf /tmp/*

    #&& apk del .build-deps

EXPOSE 8080

# Volumes
# - Conf: /etc/php/ (php-fpm.conf, php.ini)
# - Logs: /var/log/php
# - Data: /srv/www, /var/lib/php/session
