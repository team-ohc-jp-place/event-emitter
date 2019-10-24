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
    millis = int(round(time.time() * 1000))

    ret = {

        'org': '1',
        'product': 'V',
        'cardNumber':CARD_NO[random.randint(0,5)],
        'txnTS': millis,
        'txnCntry': TXN_CTRY[random.randint(0,8)],
        'txnType': TXN_TYPE[random.randint(0,4)],
        'pos':POS[random.randint(0,2)],
        'mcc': 'MCC',
        'merchId': MERCH_ID[random.randint(0,2)],
        'destCard':CARD_NO[random.randint(0,5)],
        'txnAmt': 1000.0,
        'transactionId':'TRAN'+str(random.randint(0,10000)),
        "dataWeight1": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight2": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight3": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight4": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight5": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight6": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight7": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight8": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight9": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight10": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight11": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight12": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight13": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight14": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight15": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight16": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight17": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight18": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight19": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight20": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight21": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight22": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight23": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight24": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight25": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight26": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight27": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight28": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight29": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight30": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight31": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight32": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight33": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight34": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight35": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight36": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight37": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight38": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight39": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight40": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight41": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight42": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight43": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight44": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight45": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight46": "abcdefghijklmnopqrstuvwxyz0123456789",
        "dataWeight47": "abcdefghijklmnopqrstuvwxyz0123456789"


    }
    return ret
def main(args):
    TXN_TS = 1562904000000
    TXN_INCREMENT = 360000

    logging.info('brokers={}'.format(args.brokers))
    logging.info('topic={}'.format(args.topic))
    logging.info('rate={}'.format(args.rate))

    logging.info('creating kafka producer')
    producer = KafkaProducer(bootstrap_servers=args.brokers)

    logging.info('begin sending events')
    cntr=1
    while True:

        TXN_TS = TXN_TS+TXN_INCREMENT
        crdNo = CARD_NO[random.randint(0,5)]

        logging.info('TransactionId {0} and Txn Timestamp {1}'.format(TXN_TS, cntr))

        producer.send(args.topic, json.dumps(generate_event(TXN_TS+TXN_INCREMENT,crdNo)).encode(), json.dumps(crdNo).encode())
        producer.send(args.histTopic, json.dumps(generate_event(TXN_TS+TXN_INCREMENT,crdNo)).encode(), json.dumps(crdNo).encode())
        cntr = int(cntr) + 1
        time.sleep(1.0 / 100)

def get_arg(env, default):
    return os.getenv(env) if os.getenv(env, '') is not '' else default


def parse_args(parser):
    args = parser.parse_args()
    args.brokers = get_arg('KAFKA_BROKERS', args.brokers)
    args.topic = get_arg('KAFKA_TOPIC', args.topic)
    args.rate = get_arg('RATE', args.rate)
    args.histTopic = get_arg('HIST_TOPIC', args.rate)
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
        '--hist-topic',
        help='Topic to publish to, env variable KAFKA_TOPIC',
        default='hist-input-stream')
    parser.add_argument(
        '--rate',
        type=int,
        help='Lines per second, env variable RATE',
        default=1)
    args = parse_args(parser)
    main(args)
    logging.info('exiting')
