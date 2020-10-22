FROM ubuntu:18.04

# Make sure dependencies are installed
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get install -y python3-setuptools
RUN apt install -y default-jre
RUN pip3 install setuptools --upgrade

# Put the source files in the build container
COPY . /src/

# Set working directory to where we want to run install commands from
WORKDIR /src

# Install formattters to container
RUN python3 /src/setup.py install

# Configure environment variables into writeable directory
RUN mkdir -p /src/cache/.python-eggs
RUN chmod 777 /src/cache
ENV PYTHON_EGG_CACHE=/src/cache/.python-eggs
ENV PRE_COMMIT_HOME /src/cache

ENTRYPOINT /bin/bash
