# Dockerfile has three Arguments: base, tag, branch
# base - base image (default: debian)
# tag - tag for base mage (default: stable-slim)
# branch - user repository branch to clone (default: master)
#
# To build the image:
# $ docker build -t <dockerhub_user>/<dockerhub_repo> --build-arg arg=value .
# or using default args:
# $ docker build -t <dockerhub_user>/<dockerhub_repo> .

# set the base image. default is debian, optional ubuntu
ARG base=debian
# set the tag (e.g. latest, stable, stable-slim : for debian)
ARG tag=stable-slim

# Base image, e.g. debian:stable-slim
FROM ${base}:${tag}

LABEL maintainer='Borja Esteban'

# What branch to clone (!)
ARG branch=master

# Which user and group to use 
ARG user=application
ARG group=standard

# Set environments
ENV LANG C.UTF-8

# Install system updates and tools
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
# Install system updates and tools
        ca-certificates \
        git && \
# Clean up & back to dialog front end
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog

# Install user app:
RUN git clone --depth 1 -b ${branch} https://github.com/BorjaEst/cicd.git app && \
# Clean up
    rm -rf /root/.cache/pip/* && \
    rm -rf /tmp/*
WORKDIR /app

# Ports to expose
EXPOSE 8443
EXPOSE 8080

# Change user context and drop root privileges
RUN groupadd -r ${group} && \
    useradd --no-log-init -r -d /app -g ${group} ${user} && \
    chown -R ${user} . 
USER ${user}

# Start default script
ENTRYPOINT [ "/app/main" ]
CMD [ "" ]

