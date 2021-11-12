# event emitter
Apache Kafkaトピックに送信するためのアプリケーション

## OpenShift へのデプロイ

```
oc new-app centos/python-36-centos7~https://github.com/team-ohc-jp-place/event-emitter \
 -e KAFKA_BROKERS=my-cluster-kafka-brokers:9092 \
 -e KAFKA_TOPIC=incoming-topic -e RATE=1 --name=emitter
```
