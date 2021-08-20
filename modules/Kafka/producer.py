from kafka import KafkaProducer, producer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
    api_version=(0,10))

producer.send("test", b'Test Message!!')
producer.flush()