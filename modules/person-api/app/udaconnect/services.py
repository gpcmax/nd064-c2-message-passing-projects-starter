import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]
        producer = KafkaProducer(
            bootstrap_servers='my-release-kafka.default.svc.cluster.local:9092',
            #client_id=CLIENT_ID,
            #value_serializer=JsonSerializer.serialize,
            api_version=(0, 10, 1)
        )
        producer1 = KafkaProducer(bootstrap_servers='my-release-kafka-0.my-release-kafka-headless.default.svc.cluster.local:9092')
        producer.send('text',bytes(str(person),'utf-8'))
        producer.flush()
        producer1.send('text',bytes(str(person),'utf-8'))
        producer1.flush()
        logger.warning("New Person Added")
        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()
