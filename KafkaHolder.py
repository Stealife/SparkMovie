#!/usr/bin/env python
import threading, logging, time
import multiprocessing

from kafka import KafkaConsumer, KafkaProducer

debug = False

class Producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='163.5.220.83:9092')
        if debug :
            while True:
                producer.send('my-topic', b"test")
                producer.send('my-topic', b"\xc2Hola, mundo!")
                time.sleep(1)
        else:
            producer.send('my-topic', b"Mundo does it all")

class Consumer(multiprocessing.Process):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='163.5.220.83:9092',
                                 auto_offset_reset='earliest')
        consumer.subscribe(['my-topic'])

        for message in consumer:

            print ("Message in consumer ", message.value)


def main():
    tasks = [
        Producer(),
        Consumer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(name)s:%(thread)d:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()
