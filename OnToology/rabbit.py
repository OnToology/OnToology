import json
import pika
import os
import subprocess
import sys
import hashlib
import time
import logging
import threading
import functools
from TPool.TPool import Pool
from threading import Lock
from multiprocessing import Process


lock = Lock()
locked_repos = []
connection = None


def set_config(logger, logdir=""):
    """
    :param logger: logger
    :param logdir: the directory log
    :return:
    """
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


def run_rabbit():
    """
    Run the rabbit consumer
    :return:
    """
    if 'rabbit_processes' in os.environ:
        try:
            num = int(os.environ['rabbit_processes'])
            if 'virtual_env_dir' in os.environ:
                comm = "nohup %s %s %s %s" % (os.path.join(os.environ['virtual_env_dir'], 'bin', 'python'),
                                              os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rabbit.py'),
                                              str(num), ' &')
            else:
                comm = "nohup python %s %s %s" % (
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rabbit.py'), str(num),
                '&')
            logger.debug("run_rabbit> comm: " + comm)
            subprocess.Popen(comm, shell=True)
        except:
            logger.error('run_rabbit> The rabbit_processes is: <%s>' % str(os.environ['rabbit_processes']))
    else:
        logger.debug('run_rabbit> rabbit_processes is not in environ')


def send(message_json):
    """
    :param message:
    :return:
    """
    global logger
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
    channel = connection.channel()
    queue = channel.queue_declare(queue=queue_name, durable=True, auto_delete=False)
    logger.debug("send> number of messages in the queue is: "+str(queue.method.message_count))
    message = json.dumps(message_json)
    logger.debug("send> sending message")
    logger.debug(message)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    connection.close()
    num = get_num_of_processes_of_rabbit()
    if num < 1:
        logger.warning("send> RESTART -- number of processes were: "+str(num))
        run_rabbit()


def get_pending_messages():
    """
    get number of pending messages
    :return:
    """
    global logger
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
    except:
        msg = "exception 1 in connecting"
        logger.debug(msg)
        # print(msg)
        time.sleep(3)
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
        except:
            logger.debug(msg+" for the second time")
            return -1
    channel = connection.channel()
    queue = channel.queue_declare(queue=queue_name, durable=True, auto_delete=False)
    num = queue.method.message_count
    connection.close()
    return num


def get_num_of_processes_of_rabbit():
    """
    :return:
    """
    import os
    out = os.popen('ps -ef | grep rabbit.py').read()
    lines = out.split('\n')
    one = False
    for line in lines:
        if 'python' in line and 'rabbit.py' in line:
            print("line: ")
            print(line)
            p_tokens = line.split('rabbit.py')
            if len(p_tokens) > 1:
                tokens = p_tokens[1].strip().split(' ')
                if tokens[0].strip().isdigit():
                    return int(tokens[0].strip())
                else:
                    print("ptokens: ")
                    print(p_tokens)
                    print("tokens: ")
                    print(tokens)
                    # return 1
                    one = True
    if one:
        return 1
    return -1


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
    global logger
    try:
        j = json.loads(body)
        if j['action'] in ['magic', 'change_conf', 'publish']:
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
                if j['action'] == 'magic':
                    p = Process(target=handle_action, args=(j,))
                    p.start()
                    p.join()
                    # handle_action(j)
                elif j['action'] == 'change_conf':
                    p = Process(target=handle_conf_change, args=(j,))
                    p.start()
                    p.join()
                    # handle_conf_change(j)
                elif j['action'] == 'publish':
                    p = Process(target=handle_publish, args=(j,))
                    p.start()
                    p.join()
                    # handle_publish(j)
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
        print("Message: "+str(body))
        logger.error("ERROR: "+str(e))
        logger.error("Message: "+str(body))


def handle_publish(j):
    """
    :param j:
    :return:
    """
    global logger
    logger.debug('handle_publish> going for previsual')
    try:
        autoncore.previsual(useremail=j['useremail'], target_repo=j['repo'])
    except Exception as e:
        logger.error('handle_publish> ERROR in previsualisation: '+str(e))
        return
    logger.debug('handle_publish> going for publish')
    try:
        autoncore.publish(name=j['name'], target_repo=j['repo'], ontology_rel_path=j['ontology_rel_path'],
                          useremail=j['useremail'])
    except Exception as e:
        logger.error('handle_publish> ERROR in publication: '+str(e))
        return
    logger.debug('handle_publish> done')


def handle_action(j):
    """
    :param j:
    :return:
    """
    global logger
    import autoncore
    try:
        repo = j['repo']
        if j['action'] == 'magic':
            logger.debug("going for magic: "+str(j))
            try:
                autoncore.git_magic(j['repo'], j['useremail'], j['changedfiles'])
                logger.debug("magic success")
            except Exception as e:
                logger.error("Exception in magic for repo: "+j['repo'])
                logger.error(str(e))
                print("Exception in magic for repo: "+j['repo'])
                print(str(e))
            logger.debug("magic is done")
        else:
            logger.error("Invalid magic redirect: ")
            logger.error("Invalid magic redirect with j: "+str(j))
    except Exception as e:
        logger.error("Exception 2 ")
        logger.error("Exception 2 for magic: "+str(e))
        logger.error("Exception for j: "+str(j))


def handle_conf_change(j):
    """
    :param j:
    :return:
    """
    global logger
    import autoncore
    data = j['data']
    if j['action'] == 'change_conf':
        for onto in j['ontologies']:
            logger.debug('inside the loop')
            ar2dtool = onto + '-ar2dtool' in data
            # logger.debug('ar2dtool: ' + str(ar2dtool))
            widoco = onto + '-widoco' in data
            # print 'widoco: ' + str(widoco)
            oops = onto + '-oops' in data
            # logger.debug('oops: ' + str(oops)
            logger.debug('will call get_conf')
            new_conf = autoncore.get_conf(ar2dtool, widoco, oops)
            logger.debug('will call update_file')
            o = 'OnToology' + onto + '/OnToology.cfg'
            try:
                logger.debug("target_repo <%s> ,  path <%s> ,  message <%s> ,   content <%s>" % (
                    j['repo'], o, 'OnToology Configuration', new_conf))
                autoncore.update_file(j['repo'], o, 'OnToology Configuration', new_conf)
                logger.debug('configuration is changed for file for ontology: '+onto)
            except Exception as e:
                logger.error('Error in updating the configuration: ' + str(e))
                # return render(request, 'msg.html', {'msg': str(e)})
                return

        logger.debug('Configuration changed')


def ack_message(channel, delivery_tag):
    """Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    global logger
    if channel.is_open:
        channel.basic_ack(delivery_tag)
        logger.debug("Channel is acked!")
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        logger.debug("Channel is closed!")


def start_pool(num_of_thread=1):
    """
    :param num_of_thread:
    :return:
    """
    global logger
    threads = []
    for i in range(num_of_thread):
        th = threading.Thread(target=single_worker, args=(i,))
        th.start()
        logger.debug("spawn: "+str(i))
        threads.append(th)
    logger.debug("total spawned: "+str(threads))
    for th in threads:
        th.join()
    logger.error("ALL ARE CONSUMED ..")


def single_worker(worker_id):
    """
    :param worker_id:
    :return:
    """
    global lock
    global logger
    logger.debug('worker_id: '+str(worker_id))
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
    channel = connection.channel()
    queue = channel.queue_declare(queue=queue_name, durable=True, auto_delete=False)
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

