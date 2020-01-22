# Using multi stage to prevent keeping a second copy of
# the package in the image
# See current Dockerfile_dev in the tests/build_layer_image dir to
# get the FROM layer
FROM centos:7.6.1810
MAINTAINER P-O Quirion <pierre-olivier.quirion@calculquebec.ca>
RUN yum -y update && yum -y install epel-release
RUN yum -y install \
 git python3.x86_64 \
 libffi-devel.x86_64 gcc-c++.x86_64 \
 python3-devel.x86_64 openssl-devel \
 libxml2-devel.x86_64 libxslt-devel.x86_64  libcurl-devel.x86_64 make gcc \ 
 && pip3 install --upgrade pip setuptools

ENV INGEST_V=v1.3.0
RUN pip install git+https://github.com/CanDIG/candig-ingest.git@${INGEST_V}#egg=candig_ingest \
  gevent

COPY . /tmp/server
RUN cd /tmp/server/ && pip install .

RUN mkdir /data
WORKDIR /data
RUN mkdir  mkdir candig-example-data \
  && touch access_list.tsv

RUN curl -Lo /tmp/mock_data.json  https://github.com/CanDIG/candig-ingest/releases/download/${INGEST_V}/mock_data.json \
 && ingest candig-example-data/registry.db mock_data /tmp/mock_data.json


FROM centos:7.6.1810
RUN yum -y update && yum -y install epel-release
RUN yum -y install  \
 python3.x86_64 openssl-devel \
 && yum clean all \
 && rm -rf /var/cache/yum


RUN mkdir /etc/candig && chmod 777 /etc/candig

RUN mkdir -p /opt/candig_server/

# 0 is the first stage
COPY --from=0 /data /data
COPY --from=0 /usr/local /usr/local

WORKDIR /data
EXPOSE 80

ENTRYPOINT ["candig_server", "--host", "0.0.0.0", "--port", "80"]
CMD  ["--workers", "1",  "--gunicorn", "-c", "NoAuth"]
