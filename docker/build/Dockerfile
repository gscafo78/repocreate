# Use the official Python image from the Docker Hub
FROM python:3.9-slim-buster

# Maintainer information
LABEL maintainer="Giovanni Scafetta <giovanni.scafetta@gmx.com>"

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev libffi-dev git bash cron wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

    # Clone the Git repository
RUN git clone https://github.com/gscafo78/repocreate.git /data

# Set the working directory to the cloned repository
WORKDIR /data

# Copy template file
COPY ./repocreate_template.json /repocreate_template.json

# Create repository directory
RUN mkdir /repository

# Copy the entrypoint script
COPY ./entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define a volume
VOLUME [ "/data", "/repository" ]

# CMD to start entrypoint
CMD ["/bin/bash", "/entrypoint.sh"]
