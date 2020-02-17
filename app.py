import argparse
import json
import logging
import os
import random
import time
import uuid

from kafka import KafkaProducer

EVENT_TEMPLATES = [

    {  "eventValue": "AIRLINES", "eventSource": "WEBSITE"},
    { "eventValue": "MERCHANDISE", "eventSource": "POS"},
    {  "eventValue": "HOTEL", "eventSource": "POS"},
    { "eventValue": "ONLINE_PURCHASE", "eventSource": "WEBSITE"},
    { "eventValue": "UTILITIES", "eventSource": "WEBSITE"},
    { "eventValue": "RESTAURANTS", "eventSource": "WEBSITE"},
    { "eventValue": "OTHERS", "eventSource": "WEBSITE"}

]


CUSTOMER = [


    'CUST898976',
    'CUST898700',
    'CUST898990',
    'CUST892220',
    'CUST898656',
    'CUST894320'
]

def generate_event():
    ret = EVENT_TEMPLATES[random.randint(0, 6)]
    return ret




def main(args):
    logging.info('brokers={}'.format(args.brokers))
    logging.info('topic={}'.format(args.topic))
    logging.info('rate={}'.format(args.rate))

    logging.info('creating kafka producer')
    producer = KafkaProducer(bootstrap_servers=args.brokers)

    logging.info('begin sending events')
    while True:
        event = generate_event()
        customer = CUSTOMER[random.randint(0, 5)]
        logging.info('Customer %s :: Event%s',customer,event)
        producer.send(args.topic, json.dumps(event).encode(), json.dumps(customer).encode())
        time.sleep(10.0)
    logging.info('end sending events')




def get_arg(env, default):
    return os.getenv(env) if os.getenv(env, '') is not '' else default


def parse_args(parser):
    args = parser.parse_args()
    args.brokers = get_arg('KAFKA_BROKERS', args.brokers)
    args.topic = get_arg('KAFKA_TOPIC', args.topic)
    args.rate = get_arg('RATE', args.rate)
    return args


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('starting kafka-openshift-python emitter')
    parser = argparse.ArgumentParser(description='emit some stuff on kafka')
    parser.add_argument(
        '--brokers',
        help='The bootstrap servers, env variable KAFKA_BROKERS',
        default='localhost:9092')
    parser.add_argument(
        '--topic',
        help='Topic to publish to, env variable KAFKA_TOPIC',
        default='event-input-stream')
    parser.add_argument(
        '--rate',
        type=int,
        help='Lines per second, env variable RATE',
        default=1)
    args = parse_args(parser)
    main(args)
    logging.info('exiting')
