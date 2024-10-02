#!/bin/bash

# Move configuration files if they exist in /tmp
if [ -f "/tmp/repocreate.json" ] ; then
    mv /tmp/repocreate.json /data/repocreate.json
else
    echo "Missing configuration files in /tmp"
    exit 1
fi

# Check if the CRON_EXPRESSION environment variable is set
if [ -z "$CRON_EXPRESSION" ]; then
  echo "CRON_EXPRESSION is not set. Exiting."
  exit 1
fi

# Create the crontab file dynamically
echo "$CRON_EXPRESSION python /repocreate.py --run >> /var/log/cron.log 2>&1" > /etc/crontabs/root

# Start the cron daemon
crond -f -l 2