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
     "custId":"CUST8888",
     "transactionAmount":5000,
     "transactionDate":1619019292673,
     "merchantName":"MERCH0002",
     "transactionCountry":"CHINA"

    },

    {
         "custId":"CUST99999",
         "transactionAmount":1000,
         "transactionDate":1619019292673,
         "merchantName":"MERCH7899",
         "transactionCountry":"SYRIA"

        },
        {
             "custId":"CUST8888",
             "transactionAmount":6000,
             "transactionDate":1619019292673,
             "merchantName":"MERCH7777",
             "transactionCountry":"UK"

            },
            {
                 "custId":"CUST44434",
                 "transactionAmount":1200,
                 "transactionDate":1619019292673,
                 "merchantName":"MERCH0007",
                 "transactionCountry":"SUDAN"

                }

]


CUSTOMER = [


    'CUST44434',
    'CUST8888',
    'CUST99999',
    'CUST8888'
]

def generate_event():
    ret = EVENT_TEMPLATES[random.randint(0, 3)]
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
        customer = CUSTOMER[random.randint(0, 3)]
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
