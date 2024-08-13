FROM python:3.13-rc-alpine3.19

WORKDIR /app

COPY cron/cronjobs /etc/crontabs/root

# Copy over files needed to run drive backup
COPY drive_backup/* .
RUN pip install --upgrade -r requirements.txt

# Copy over files to renew letsencrypt certificates

CMD ["crond", "-f", "-d", "8"]
