FROM themattrix/tox-base

MAINTAINER ExOLever <devops@exolever.com>

COPY . .

ARG SKIP_TOX=false
RUN bash -c " \
    if [ -f 'install-prereqs.sh' ]; then \
        bash install-prereqs.sh; \
    fi && \
    if [ $SKIP_TOX == false ]; then \
        TOXBUILD=true tox; \
    fi"
