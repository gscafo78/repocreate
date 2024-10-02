#!/bin/sh

# # Move configuration files if they exist in /tmp
# if [ -f "/tmp/repocreate.json" ] ; then
#     mv /tmp/repocreate.json /data/repocreate.json
# else
#     echo "Missing configuration files in /tmp"
#     exit 1
# fi

# Check if the CRON environment variable is set
if [ -z "$CRON" ]; then
  echo "CRON is not set. Exiting."
  exit 1
fi

# Create the crontab file dynamically
echo "$CRON python /repocreate.py --run > /var/log/cron.log 2>&1" > /etc/crontabs/root

# Ensure the log file exists
touch /var/log/cron.log

# Start the cron daemon
crond

# Tail the log file to show output
tail -f /var/log/cron.log
