FROM python:3.6
MAINTAINER gmm
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
COPY default_scrapyd.conf /usr/local/lib/python3.6/site-packages/scrapyd/
CMD ["scrapyd"]