FROM python:3.10.5-buster

RUN pip install slack_sdk
RUN pip install markdown

RUN wget -L -O /usr/local/bin/jattach \
  https://github.com/apangin/jattach/releases/download/v2.0/jattach && \
  chmod +x /usr/local/bin/jattach

ADD slack_message.py /slack_message.py
ADD bash_command.sh /bash_command.sh

CMD ["python", "/slack_message.py"]
