FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
COPY logs logs
COPY src src
RUN pip3 install -r requirements.txt

CMD [ "python3", "-m", "src" ]