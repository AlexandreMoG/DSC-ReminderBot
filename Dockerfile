#
# reminder_bot Dockerfile
#
# ===
# TODO:
#
# ===
# A.Moral       apr.28  creation
#

ARG PYTHON_REV="latest"
FROM python:${PYTHON_REV}

# Maintainer
LABEL MAINTAINER="Alexandre.MoG <https://github.com/AlexandreMoG>"

# build ARGS
ARG APP_DIR="/app"

# Switch to bash as default shell
SHELL [ "/bin/bash", "-c" ]

# ENV args
ENV APP_DIR="${APP_DIR}"\
    DOCKYARD="/dockyard"

# Working directory
WORKDIR ${APP_DIR}

# Copy configuration directory
COPY ${DOCKYARD} ${DOCKYARD}

# Copy application
COPY ${APP_DIR} ${APP_DIR}

# Various packages to install and final update
RUN \
    env \
    && apt-get -y update \
    && apt-get -y --allow-unauthenticated install \
        git \
        python3-dev \
        python3-pip \
    # python packages
    && pip3 install -r ${DOCKYARD}/requirements.txt \
    # Final cleaning
    && apt-get clean

CMD ["python3","reminder_bot.py"]
