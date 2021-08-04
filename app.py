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
        "kogitodmnmodelname": "TransactionMonitoringDMN",
        "kogitodmnmodelnamespace": "https://kiegroup.org/dmn/_EED47FB5-8A7C-44F3-A786-563FD2DAF015",
        "data": {
            "Transaction": { "transactionAmount": 9500,
                             "transactionCountry":"US",
                             "merchantType": "MERCH336",
                             "transactionType":"Web" ,
                             "transactionId":1626891159443,
                             "paymentMode":"savings"},
            "Customer": {
                "averageTransactionAmount": 300,
                "riskIndex": 1.7,
                "marriage": false,
                "jobChange": false,
                "cityChange": false,
                "customerId": "CUST898920"
            }
        }
    }
]


CUSTOMER = [


    'CUST8788'
]

def generate_event():
    ret = EVENT_TEMPLATES[0]
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
        time.sleep(100000.0)
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
