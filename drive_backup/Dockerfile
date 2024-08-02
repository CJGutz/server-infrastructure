FROM python:3.13-rc-alpine3.19

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt

COPY cronjobs /etc/crontabs/root

COPY . .

CMD ["crond", "-f", "-d", "8"]
