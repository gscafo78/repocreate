# Use the official Python image from the Docker Hub
FROM python:3.9.20-alpine3.19

# Maintainer information
LABEL maintainer="Giovanni Scafetta <giovanni.scafetta@gmx.com>"

# Install dependencies
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev git bash

# Clone the Git repository
RUN git clone https://github.com/gscafo78/repocreate.git /app/repo

# Set the working directory to the cloned repository
WORKDIR /app/repo

# COPY *.cfg /opt
COPY ./*.json /tmp

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point
ENTRYPOINT ["/entrypoint.sh"]