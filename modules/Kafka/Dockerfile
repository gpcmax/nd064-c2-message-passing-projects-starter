FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
RUN python -m pip install -U pip
RUN apk update && apk add --virtual build-dependencies build-base gcc wget
RUN pip3 install --upgrade setuptools
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
CMD ["python","consumer.py"]