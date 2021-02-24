FROM python:3.9.0

WORKDIR /opt/api

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /tools/wait-for-it.sh
RUN chmod +x /tools/wait-for-it.sh

# install requirements
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# copy sources
COPY ./app ./
COPY ./setup.cfg ./uwsgi.ini ./

# set environments
ENV PYTHONUNBUFFERED=1

CMD uwsgi -i uwsgi.ini
