FROM ubuntu
RUN groupadd -r myapp && useradd -r -g myapp myapp
ENV USER_ID=root USER_PASS=test MYSQL_URL=mydb CELERY_BROKER_URL=amqp://guest:guest@amqp:5672//
RUN apt-get -y update && apt-get install -y mysql-client python-pip python-dev
RUN apt-get -y install libmysqlclient-dev
RUN apt-get -y install netcat
COPY ./mydb /mydb/
WORKDIR /mydb
RUN pip install -r requirements.txt
RUN chmod +x init_db.py
COPY ./myservice /myservice/
WORKDIR /myservice
USER myapp
EXPOSE 5000
CMD python2 upload_service.py
