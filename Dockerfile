ARG PYTHON_VERSION=3.7.7

FROM python:${PYTHON_VERSION}-alpine
WORKDIR /app
ENV LC_ALL=C.UTF-8 \
  LANG=C.UTF-8 \
  TZ="Europe/Zurich"
RUN apk --no-cache update && \
  apk --no-cache add \
  jpeg-dev \
  zlib-dev \
  gettext \
  build-base \
  libxml2-dev \
  libxslt-dev \
  # For Package build only
  libffi-dev \
  openssl-dev \
  rsync \
  # Only for Postgresql Projects
  postgresql-dev \
  # Only for MySQL Projects
  # mariadb-dev \
  tzdata \
  && cp /usr/share/zoneinfo/Europe/Zurich /etc/localtime \
  && echo $TZ > /etc/timezone \
  && apk del tzdata \
  &&  rm -fr /var/cache/apk/*