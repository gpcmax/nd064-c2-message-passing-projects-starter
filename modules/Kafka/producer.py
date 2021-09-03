from kafka import KafkaProducer, producer

producer = KafkaProducer(bootstrap_servers='localhost:9092', api_version=(0,10,1))
message=dict({'first_name':'Billy','last_name':'Joel','company_name':'Music Inc'})
producer.send('test', bytes(str(message)),'utf-8')
producer.flush()