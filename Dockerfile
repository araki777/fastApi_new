FROM postgres:14-alpine

COPY ./init-scripts /docker-entrypoint-initdb.d/