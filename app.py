import argparse
import json
import logging
import os
import random
import time
import uuid

from kafka import KafkaProducer

EVENT_TEMPLATES = [

    {
        "specversion": "1.0",
        "id": "a89b61a2-5644-487a-8a86-144855c5dce8",
        "source": "SomeEventSource",
        "type": "DecisionRequest",
        "subject": "TheSubject",
        "kogitodmnmodelname": "Order_Conversion",
        "kogitodmnmodelnamespace": "https://github.com/kiegroup/drools/kie-dmn/_A4BCA8B8-CF08-433F-93B2-A2598F19ECFF",
        "data": {
            "OrderType": "E",
            "OrderItemName": "Lime",
            "Quantity": 100,
            "Price": 3.69,
            "ShipmentAddress": "541-428 Nulla Avenue",
            "ZipCode": "4286"
        }
    },
    {
        "specversion": "1.0",
        "id": "a89b61a2-5644-487a-8a86-144855c5dce8",
        "source": "SomeEventSource",
        "type": "DecisionRequest",
        "subject": "TheSubject",
        "kogitodmnmodelname": "Order_Conversion",
        "kogitodmnmodelnamespace": "https://github.com/kiegroup/drools/kie-dmn/_A4BCA8B8-CF08-433F-93B2-A2598F19ECFF",
        "data": {
            "OrderType": "E",
            "OrderItemName": "Lemon Bar",
            "Quantity": 17,
            "Price": 0.09,
            "ShipmentAddress": "Ap #249-5876 Magna. Rd.",
            "ZipCode": "I9E 0JN"
        }
    }
]


def generate_event():
    ret = EVENT_TEMPLATES[random.randrange(2)]
    return ret


def main(args):
    logging.info('brokers={}'.format(args.brokers))
    logging.info('topic={}'.format(args.topic))
    logging.info('rate={}'.format(args.rate))

    logging.info('creating kafka producer')
    producer = KafkaProducer(bootstrap_servers=args.brokers)

    logging.info('begin sending events')
    while True:

        producer.send(args.topic,json.dumps(generate_event()).encode() , 'cust567'.encode())
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
