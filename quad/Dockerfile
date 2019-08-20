FROM continuumio/anaconda

MAINTAINER John Beieler <jbeieler1@jhu.edu>

RUN apt-get update
RUN apt-get install -y curl
RUN echo 'asdasf'
RUN cat /etc/apt/sources.list
RUN apt-get install apt-transport-https

RUN echo "deb https://deb.debian.org/debian stable main \n deb https://deb.debian.org/debian-security stable/updates main" > /etc/apt/sources.list

RUN cat /etc/apt/sources.list

RUN apt-get clean && apt-get update &&  apt-get autoclean
RUN apt-get install -y --force-yes build-essential #python-dev netcat
RUN apt-get install -y python-dev
RUN apt-get install -y netcat

ADD . /src
RUN cd /src; /opt/conda/bin/pip install -r requirements.txt

RUN chmod -x /src/launch.sh
CMD sh /src/launch.sh
