FROM python:latest

RUN pip install --no-cache-dir loudify



# tell the port number the container should expose
EXPOSE 5555

# run the command
CMD ["loudify-broker -p 5555 -vv"]
# CMD . /opt/venv/bin/activate && exec python myapp.py