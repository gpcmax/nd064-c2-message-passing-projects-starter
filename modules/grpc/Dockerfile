FROM python:3.7.4

WORKDIR .

#RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5004

COPY . .
CMD ["python", "main.py", "--port", "5004"]