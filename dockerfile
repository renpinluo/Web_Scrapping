FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt install -y python3 python3-pip libxml2-dev libxmlsec1-dev

RUN apt-get install -y xvfb
RUN apt-get install -y wget
RUN apt-get install -y openssl build-essential xorg
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar xvJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN cp wkhtmltox/bin/wkhtmlto* /usr/bin/

RUN apt-get install -y libssl-dev
COPY requirements.txt /

RUN pip3 install -r requirements.txt

WORKDIR /

#COPY test-data /test-data
#COPY tests /tests
COPY main.py /
COPY scrape.py /
COPY websites.pkl /
COPY config.py /
COPY metadata_prompts.py /

#RUN python3 gen_py_test.py 
# add tests to path
ENV PYTHONPATH "${PYTHONPATH}:/tests"

#WORKDIR /tests
CMD [ "python3","main.py" ]