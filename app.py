import argparse
import json
import logging
import os
import random
import time
import uuid

from kafka import KafkaProducer

CARD_NO= [
    "2345796540876432", "7766554433221198", "9856342187654321", "7777744433667790"
        , "6538764975321765", "086543226688908"]






TXN_CTRY = [

    'SG',
    'TH',
    'PH',
    'MY',
    'HK',
    'BR',
    'US',
    'CA',
    'IN'
]



POS = [

    '9100',
    '1234',
    '1111'
]


TXN_TYPE = [

    'Purchase',
    'ATM',
    'MOBILE_CHG',
    'cardReissue',
    'addressChange'
]

MERCH_ID = [
    'MERCH1','MERCH2','MERCH3'
]




def generate_event(TXN_TS, CUST):

    ret = {
        'org': '1',
        'product': 'V',
        'cardNumber': CUST,
        'txnTS': TXN_TS,
        'txnCntry': TXN_CTRY[random.randint(0,8)],
        'txnType': TXN_TYPE[random.randint(0,4)],
        'pos':POS[random.randint(0,2)],
        'mcc': 'MCC',
        'merchId': MERCH_ID[random.randint(0,2)],
        'destCard':CARD_NO[random.randint(0,5)]


    }
    return ret
def main(args):
    TXN_TS = 1562904000000
    TXN_INCREMENT = 100000
    logging.info('brokers={}'.format(args.brokers))
    logging.info('topic={}'.format(args.topic))
    logging.info('rate={}'.format(args.rate))

    logging.info('creating kafka producer')
    producer = KafkaProducer(bootstrap_servers=args.brokers)

    logging.info('begin sending events')
    while TXN_TS < time.time()*1000:
        TXN_TS = TXN_TS+TXN_INCREMENT
        crdNo = CARD_NO[random.randint(0,5)]
        producer.send(args.topic, json.dumps(generate_event(TXN_TS+TXN_INCREMENT,crdNo)).encode(), json.dumps(crdNo).encode())

    logging.info('crdNo')





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
