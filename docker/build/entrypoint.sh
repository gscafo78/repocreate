#!/bin/sh

if [ ! -f /data/repocreate.json ]; then
  cp /repocreate_template.json /data/repocreate.json
fi

# Check if the CRON environment variable is set
if [ -z "$CRON" ]; then
  echo "CRON is not set. Exiting."
  exit 1
fi

# Create the crontab file dynamically
echo "$CRON python /data/repocreate.py --run > /var/log/cron.log 2>&1" > /etc/crontabs/root

# Add a cron job to clear the log file every 7 days
echo "0 0 */7 * * echo '' > /var/log/cron.log" >> /etc/crontabs/root

# Ensure the log file exists
touch /var/log/cron.log

# Start the cron daemon
crond

# Tail the log file to show output
tail -f /var/log/cron.log