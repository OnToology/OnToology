import json
import pika
import os
import sys
import hashlib
import time
import logging
import threading
import functools
from TPool.TPool import Pool
from threading import Lock

lock = Lock()
locked_repos = []
connection = None


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


# def get_logger():
#     """
#     To be used by the different threads
#     :return:
#     """
#     if 'rabbit_log_dir' in os.environ:
#         log_dir = os.environ['rabbit_log_dir']
#         logger = logging.getLogger(__name__)
#         set_config(logger, log_dir)
#     else:
#         logger = logging.getLogger(__name__)
#         set_config(logger)
#     return logger


def send(message_json):
    """
    :param message:
    :return:
    """
    # logger = get_logger()
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


# def callback(ch, method, properties, body, args):
#     """
#     Spawn a thread to consume it
#     :param ch:
#     :param method:
#     :param properties:
#     :param body:
#     :return:
#     """
#     connection_ = args[0]
#     delivery_tag = method.delivery_tag
#     th = threading.Thread(target=callback_handler, args=(ch, method, properties, body, delivery_tag, connection_))
#     th.start()
#     ch.basic_ack(delivery_tag=method.delivery_tag)


def callback(ch, method, properties, body):
    """
    Consume messages from the ready queue
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    global lock
    try:
        j = json.loads(body)
        if j['action'] == 'magic':
            repo_name = j['repo']
            logger.debug('callback repo: '+repo_name)
            lock.acquire()
            busy = repo_name in locked_repos
            if not busy:
                logger.debug('not busy repo: ' + repo_name)
                locked_repos.append(repo_name)
            else:
                logger.debug('is busy repo: ' + repo_name)
            lock.release()

            if busy:
                logger.debug(repo_name+" is busy --- ")
                time.sleep(5)
                ch.basic_nack(delivery_tag=method.delivery_tag)
            else:
                logger.debug(" ---  Consuming: " + repo_name)
                logger.debug(body)
                handle_action(j)
                logger.debug(repo_name+" Completed!")
                lock.acquire()
                logger.debug(repo_name+" to remove it from locked repos")
                locked_repos.remove(repo_name)
                logger.debug(repo_name+" is removed")
                lock.release()
                logger.debug(repo_name+" is sending the ack")
                ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("ERROR: "+str(e))
        logger.error("ERROR: "+str(e))


def handle_action(j):
    """
    :param j:
    :return:
    """
    import autoncore
    if j['action'] == 'magic':
        logger.debug("going for magic")
        autoncore.git_magic(j['repo'], j['useremail'], j['changedfiles'])
        logger.debug("magic is done")


def ack_message(channel, delivery_tag):
    """Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        channel.basic_ack(delivery_tag)
        logger.debug("Channel is acked!")
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        logger.debug("Channel is closed!")


# def callback_handler(ch, method, properties, body, delivery_tag, connection_):
#     """
#     :param body:
#     :return:
#     """
#     global lock
#
#     # connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
#     # ch = connection.channel()
#     # queue = channel.queue_declare(queue=queue_name, durable=True, auto_delete=True)
#
#     try:
#         import autoncore
#         autoncore.django_setup_script()
#         j = json.loads(body)
#         repo_name = j['repo']
#         logger.debug('callback repo: '+repo_name)
#         lock.acquire()
#         busy = repo_name in locked_repos
#         if not busy:
#             logger.debug('not busy repo: ' + repo_name)
#             locked_repos.append(repo_name)
#         else:
#             logger.debug('is busy repo: ' + repo_name)
#         lock.release()
#         if busy:
#             logger.debug(repo_name+" is busy --- ")
#             time.sleep(5)
#         else:
#             logger.debug(" ---  Consuming: " + repo_name)
#             logger.debug(body)
#             handle_action(j)
#             logger.debug(repo_name+" Completed!")
#             lock.acquire()
#             logger.debug(repo_name+" to remove it from locked repos")
#             locked_repos.remove(repo_name)
#             logger.debug(repo_name+" is removed")
#             lock.release()
#             logger.debug(repo_name+" is sending the ack")
#             ch.basic_ack(delivery_tag=delivery_tag)
#             # cb = functools.partial(ack_message, channel, delivery_tag)
#             # connection_.add_callback_threadsafe(cb)
#     except Exception as e:
#             logger.error("ERROR: "+str(e))


def start_pool(num_of_thread=1):
    # logger = get_logger()
    # params = []
    # for i in range(num_of_thread):
    #     params.append((i,))
    # pool = Pool(max_num_of_threads=num_of_thread, func=single_worker, params_list=params, logger=logger)
    # logger.info("spawned %d threads" % num_of_thread)
    # pool.run()
    threads = []
    for i in range(num_of_thread):
        th = threading.Thread(target=single_worker, args=(i,))
        th.start()
        logger.debug("spawn: "+str(i))
        threads.append(th)
    logger.debug("total spawned: "+str(threads))
    for th in threads:
        th.join()


def single_worker(worker_id):
    global lock
    # logger = get_logger()
    logger.debug('worker_id: '+str(worker_id))
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
    channel = connection.channel()
    queue = channel.queue_declare(queue=queue_name, durable=True, auto_delete=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print("Rabbit consuming is started ... "+str(worker_id))
    logger.debug("Setting the logger ..."+str(worker_id))
    logger.debug("test connection ..."+str(channel.is_open))
    logger.debug("single_worker> number of messages in the queue is: " + str(queue.method.message_count))
    channel.start_consuming()


if __name__ == '__main__':
    import autoncore
    autoncore.django_setup_script()

    if len(sys.argv) > 1:
        start_pool(int(sys.argv[1]))
    else:
        start_pool()

