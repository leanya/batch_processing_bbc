FROM python:3.9-alpine

COPY . .

RUN pip install -r requirements.txt

RUN /usr/bin/crontab /crontab.txt

CMD ["crond", "-f"]