FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
COPY src src
RUN pip3 install -r requirements.txt
RUN mkdir logs

CMD [ "python3", "-m", "src" ]
