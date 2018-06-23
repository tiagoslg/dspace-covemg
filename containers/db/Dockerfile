# From https://github.com/DSpace-Labs/dspace-dev-docker/tree/master/postgres
FROM postgres:9.6

ENV POSTGRES_DB dspace
ENV POSTGRES_USER dspace
ENV POSTGRES_PASSWORD dspace

COPY containers/db/docker-entrypoint-initdb.d/install-pgcrypto.sh /docker-entrypoint-initdb.d/