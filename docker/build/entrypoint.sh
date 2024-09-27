#!/bin/bash

# Move configuration files if they exist in /tmp
if [ -f "/tmp/openssl.cfg" ] && [ -f "/tmp/ca.cfg" ]; then
    mv /tmp/*.cfg "${certconfig}"
else
    echo "Missing configuration files in /tmp"
    exit 1
fi
