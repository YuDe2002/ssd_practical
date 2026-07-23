FROM postgres:15

# Install wget to download the password list
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Download the NCSC 100k common passwords list
RUN wget -O /tmp/common_passwords.txt \
    https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt

COPY init.sql /docker-entrypoint-initdb.d/

# The list will be loaded by init.sql via COPY command
# Ensure the file is accessible inside the container
RUN cp /tmp/common_passwords.txt /common_passwords.txt