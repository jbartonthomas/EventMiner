import json
import time
import utils
import logging

from mitie import *

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


NER = named_entity_extractor('MITIE-models/english/ner_model.dat')


def callback(ch, method, properties, body):
    data = json.loads(body)
    logger.info('Started processing content. {}'.format(data['pipeline_key']))

    process(data)

    logger.info('Finished NER tagging. {}'.format(data['pipeline_key']))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def process(data):
    publish = 'mitie'
    rabbit_publish = utils.RabbitClient(queue=publish,
                                        host='rabbitmq')
    data['ner_info'] = {}
    for sid, sent in data['sents'].iteritems():
        try:
            tokens = tokenize(sent)
            entities = NER.extract_entities(tokens)

            new_ents = []
            for e in entities:
                #MITIE returns xrange iters. Convert to tuples of ints
                r = (e[0].__reduce__()[1][0],
                     e[0].__reduce__()[1][1])
                tag = e[1]
                score = e[2]
                new_ents.append((r, tag, score))
            data['ner_info'][sid] = new_ents
        except Exception as e:
            # If something goes wrong, log it and return nothing
            logger.info(e)
            # Make sure to update this line if you change the variable names

    logger.info('Finished processing content.')

    rabbit_publish.send(data, publish)


def main():
    logger.info('... waiting ...')
    time.sleep(30)
    logger.info('... done ...')

    consume = 'ingest'
    rabbit_consume = utils.RabbitClient(queue=consume,
                                        host='rabbitmq')

    rabbit_consume.receive(callback)


if __name__ == '__main__':
    logger.info('Running...')
    main()
