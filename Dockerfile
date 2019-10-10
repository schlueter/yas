FROM python:alpine

COPY . .
RUN python setup.py install && rm -rf build dist
RUN mkdir -p /usr/local/etc/yas
COPY example-yas.yml /usr/local/etc/yas/yas.yml
CMD yas
