FROM python:3.6
MAINTAINER gmm
RUN pip install scrapyd && pip install scrapyd-client
COPY default_scrapyd.conf /usr/local/lib/python3.6/site-packages/scrapyd/
CMD ["scrapyd"]