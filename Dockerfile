FROM centos:7.6.1810
MAINTAINER P-O Quirion <pierre-olivier.quirion@calculquebec.ca>
RUN yum -y install epel-release
RUN yum -y install python36-pip.noarch \
 git \
 libffi-devel.x86_64 gcc-c++.x86_64 \
 python36-devel.x86_64 openssl-devel \
 libxml2-devel.x86_64 libxslt-devel.x86_64  libcurl-devel.x86_64 make gcc && \
 pip3 install --upgrade pip setuptools

RUN  pip install \
  git+https://github.com/CanDIG/candig-schemas.git@v1.0.0#egg=candig_schemas  \
  git+https://github.com/CanDIG/candig-server.git@ddb8afbe1089193260f1ce08f7e83214edc81c36#egg=candig_server  \
  git+https://github.com/CanDIG/candig-ingest.git@v1.3.0#egg=candig_ingest \
  gevent
#  git+https://github.com/CanDIG/candig-client.git@#egg=candig_client \

#  requests==2.7.0
RUN mkdir /data
WORKDIR /data
RUN mkdir -p server/templates \
  && touch server/templates/initial_peers.txt \
  && mkdir ga4gh-example-data \
  && touch access_list.txt
COPY mock_clinphen_1.json  /tmp/.

RUN mkdir /etc/candig && chmod 777 /etc/candig
RUN ingest ga4gh-example-data/registry.db clinical_metadata_tier /tmp/mock_clinphen_1.json

EXPOSE 80
RUN mkdir -p /opt/ga4gh_server/
# The ls forces a cash flush
ENTRYPOINT ["candig_server", "--host", "0.0.0.0", "--port", "80"]
CMD  ["--workers", "1",  "--gunicorn", "-f", "/opt/candig_server/config.py"]
# test with
# -c NoAuth --workers 1 --gunicorn