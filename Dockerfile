FROM python:latest

RUN pip install --no-cache-dir loudify



# tell the port number the container should expose
EXPOSE 5000

# run the command
# CMD ["python", "./app.py"]
# CMD . /opt/venv/bin/activate && exec python myapp.py