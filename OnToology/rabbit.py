import json
import pika
import os
import hashlib
import time
import logging


def set_config(logger, logdir=""):
    if logdir != "":
        handler = logging.FileHandler(logdir)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


queue_name = 'ontoology'

print("Will check the rabbit host \n\n\n")
if 'rabbit_host' in os.environ:
    rabbit_host = os.environ['rabbit_host']
    print("rabbit_host: "+rabbit_host)
else:
    rabbit_host = 'localhost'
    print("rabbit_host: "+rabbit_host)

if 'rabbit_log_dir' in os.environ:
    log_dir = os.environ['rabbit_log_dir']
    logger = logging.getLogger(__name__)
    set_config(logger, log_dir)
else:
    logger = logging.getLogger(__name__)
    set_config(logger)


def send(message_json):
    """
    :param message:
    :return:
    """
    # from autoncore import prepare_logger
    # prepare_logger()
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
    channel = connection.channel()
    queue = channel.queue_declare(queue=queue_name, durable=True, auto_delete=True)
    logger.debug("send> number of messages in the queue is: "+str(queue.method.message_count))
    message = json.dumps(message_json)
    logger.debug("sending message")
    logger.debug(message)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    connection.close()


def callback(ch, method, properties, body):
    """
    Consume messages from the ready queue
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    try:
        import autoncore
        autoncore.django_setup_script()

        j = json.loads(body)
        repo_name = j['repo']
        b = autoncore.is_busy(repo_name)
        if b == None:
            logger.error(repo_name+" is not found in the database")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        elif b:
            logger.debug(repo_name+" is busy")
            time.sleep(5)
        else:
            logger.debug("Consuming: " + repo_name)
            logger.debug(body)
            handle_action(j)
            logger.debug(repo_name+" Completed!")
            ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
            logger.error("ERROR: "+str(e))


def handle_action(j):
    """
    :param j:
    :return:
    """
    import autoncore
    # django_setup_script()
    if j['action'] == 'magic':
        logger.debug("going for magic")
        autoncore.git_magic(j['repo'], j['useremail'], j['changedfiles'])
        logger.debug("magic is done")


# def monitor():
#     # queue = channel.queue_declare(queue=queue_name, durable=True, auto_delete=True)
#     print(queue.method.message_count)


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
    channel = connection.channel()
    queue = channel.queue_declare(queue=queue_name, durable=True, auto_delete=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print("Rabbit consuming is started ...")
    logger.debug("Setting the logger ...")
    channel.start_consuming()
