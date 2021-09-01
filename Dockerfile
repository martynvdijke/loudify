FROM python:latest

RUN pip install --no-cache-dir loudify

WORKDIR /usr/src/app
COPY bin/broker.py .

# run the command
CMD [ "python", "./broker.py", "-p 5555", "-vv" ]

# tell the port number the container should expose
EXPOSE 5555