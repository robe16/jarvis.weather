FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Update
RUN apt-get update \
    && apt-get install -y python3 python3-pip

WORKDIR /jarvis/weather

# Bundle app source
COPY src /jarvis/weather

# Copy app dependencies
COPY requirements.txt requirements.txt

# Install app dependencies
RUN pip3 install -r requirements.txt

# Run application
CMD python3 run.py
