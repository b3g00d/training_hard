FROM celery:latest
ENV USER_ID=root USER_PASS=test MYSQL_URL=mydb CELERY_BROKER_URL=amqp://guest:guest@amqp:5672//
USER root
RUN apt-get -y update && apt-get install -y python-pip python-dev
RUN apt-get -y install libmysqlclient-dev
RUN apt-get -y install python-setuptools
RUN apt-get -y install zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk libjpeg-dev
RUN pip2 install --upgrade pip && pip2 install mysqlclient
COPY ./mydb /mydb/
COPY ./myworker/thumbing_worker.py /myworker/
WORKDIR /mydb
RUN pip2 install -r requirements.txt
WORKDIR /myworker
USER user
CMD celery worker -A thumbing_worker --loglevel=info
