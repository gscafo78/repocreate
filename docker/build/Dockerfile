# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Maintainer information
LABEL maintainer="Giovanni Scafetta <giovanni.scafetta@gmx.com>"

# Install dependencies
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev git bash dcron wget

# Clone the Git repository
RUN git clone https://github.com/gscafo78/repocreate.git /data

# Set the working directory to the cloned repository
WORKDIR /data

COPY ./repocreate_template.json /repocreate_template.json

RUN mkdir /repository

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

VOLUME [ "/data" ]

# Set the entry point
ENTRYPOINT ["/entrypoint.sh"]
