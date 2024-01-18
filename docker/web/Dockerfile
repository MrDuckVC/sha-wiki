FROM python:3.11-slim as build

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        pkg-config \
        libtidy-dev \
        libmariadb-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --upgrade pip

RUN pip3 install --no-cache-dir --no-warn-script-location \
        uwsgi \
        Django==4.2.5 \
        django-bootstrap-v5==1.0.11 \
        mysqlclient==2.2.0 \
        Pillow==10.0.1 \
        pytidylib==0.3.2


FROM python:3.11-slim as runtime_base

ENV SOCK_PATH=/var/run/python/uwsgi.sock \
    WSGI_FILE_PATH=/var/www/backend/carpedia/wsgi.py \
    WSGI_PROCESSES=4

VOLUME [ "/var/run/python" ]

WORKDIR /var/www/backend

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libtidy-dev \
        libmariadb3 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin/uwsgi /usr/local/bin/

CMD ["sh", "-c", "uwsgi --master --die-on-term --protocol uwsgi --wsgi-file $WSGI_FILE_PATH --socket $SOCK_PATH --chmod-socket=666 --processes=$WSGI_PROCESSES"]

FROM runtime_base as runtime_dev

EXPOSE 5000
EXPOSE 5678

RUN pip3 install --no-cache-dir --no-warn-script-location debugpy

CMD ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "manage.py", "runserver", "0.0.0.0:5000"]
