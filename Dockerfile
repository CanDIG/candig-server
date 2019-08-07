# Using multi stage to prevent keeping a second copy of the package in the image
FROM centos:7.6.1810
COPY . /tmp/server


FROM centos:7.6.1810
MAINTAINER P-O Quirion <pierre-olivier.quirion@calculquebec.ca>
RUN yum -y install epel-release
RUN yum -y install python36-pip.noarch \
 git \
 libffi-devel.x86_64 gcc-c++.x86_64 \
 python36-devel.x86_64 openssl-devel \
 libxml2-devel.x86_64 libxslt-devel.x86_64  libcurl-devel.x86_64 make gcc && \
 pip3 install --upgrade pip setuptools \
 && yum clean all \
 && rm -rf /var/cache/yum ~/.cache

ENV SCHEMA_V=v1.0.0 INGEST_V=v1.3.0

RUN  pip install \
  git+https://github.com/CanDIG/candig-schemas.git@${SHEMA_V}#egg=candig_schemas  \
  git+https://github.com/CanDIG/candig-ingest.git@${INGEST_V}#egg=candig_ingest \
  gevent && rm -rf ~/.cache

# 0 is the irst stage
COPY --from=0 /tmp/server /tmp/server
RUN cd /tmp/server/ && pip install . && rm -rf ~/.cache

RUN mkdir /data
WORKDIR /data
RUN mkdir -p server/templates \
  && touch server/templates/initial_peers.txt \
  && mkdir ga4gh-example-data \
  && touch access_list.txt

RUN mkdir /etc/candig && chmod 777 /etc/candig

RUN curl -Lo /tmp/mock_data.json  https://github.com/CanDIG/candig-ingest/releases/download/${INGEST_V}/mock_data.json \
 && ingest ga4gh-example-data/registry.db mock_data /tmp/mock_data.json \
 && rm /tmp/mock_data.json


EXPOSE 80
RUN mkdir -p /opt/ga4gh_server/
# The ls forces a cash flush
ENTRYPOINT ["candig_server", "--host", "0.0.0.0", "--port", "80"]
CMD  ["--workers", "1",  "--gunicorn", "-f", "/opt/candig_server/config.py"]

# test with
# -c NoAuth --workers 1 --gunicorn