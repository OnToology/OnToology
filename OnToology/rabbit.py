import json
import pika
import os
import subprocess
import sys
import hashlib
import time
import logging
import threading
from functools import partial
import functools
from TPool.TPool import Pool
# from threading import Lock
from multiprocessing import Process, Pipe, Lock
import multiprocessing


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
    logger = multiprocessing.get_logger()
    # logger = logging.getLogger(__name__)
    logger = set_config(logger, log_dir)
else:
    # logger = logging.getLogger(__name__)
    logger = multiprocessing.get_logger()
    logger = set_config(logger)


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
            print("run_rabbit> comm: " + comm)
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
    logger.debug("send> sending message: "+str(message))
    # logger.debug(message)
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


def callback2(extra, ch, method, properties, body):
    """
    Consume messages from the ready queue
    :param extra:
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """

    lock = extra['lock']
    logger = extra['logger']
    receiver = extra['receiver']
    sender = extra['sender']

    try:
        j = json.loads(body)
        if j['action'] in ['magic', 'change_conf', 'publish']:
            repo_name = j['repo']
            #logger.debug('callback repo: '+repo_name)
            lock.acquire()
            locked_repos = receiver.recv()
            busy = repo_name in locked_repos
            if not busy:
                logger.debug('not busy repo: ' + repo_name + " (" + str(method.delivery_tag) + ")")
                locked_repos.append(repo_name)
                logger.debug("start locked repos: "+str(locked_repos))
            else:
                logger.debug('is busy repo: ' + repo_name + " (" + str(method.delivery_tag) + ")")
                #logger.debug("busy ones: "+str(locked_repos))
            sender.send(locked_repos)
            lock.release()
            if busy:
                #logger.debug(repo_name+" is busy --- ")
                time.sleep(5)
                ch.basic_nack(delivery_tag=method.delivery_tag, multiple=False, requeue=True)
            else:
                logger.debug(" ---  Consuming: " + repo_name + "\n" + str(body))
                # logger.debug(body)
                if j['action'] == 'magic':
                    logger.debug('starting a magic process')
                    # p = Process(target=handle_action, args=(j, logger))
                    # p.start()
                    # p.join()
                    handle_action(j, logger)
                elif j['action'] == 'change_conf':
                    logger.debug('starting a config change process')
                    # p = Process(target=handle_conf_change, args=(j, logger))
                    # p.start()
                    # p.join()
                    handle_conf_change(j, logger)
                elif j['action'] == 'publish':
                    logger.debug('starting a publish process')
                    # p = Process(target=handle_publish, args=(j, logger))
                    # p.start()
                    # p.join()
                    handle_publish(j, logger)
                else:
                    logger.debug("starting nothing")
                logger.debug(repo_name+" Completed!")
                lock.acquire()
                locked_repos = receiver.recv()
                logger.debug(repo_name+" to remove it from locked repos")
                locked_repos.remove(repo_name)
                logger.debug(repo_name+" is removed")
                logger.debug("locked repos: ")
                logger.debug(str(locked_repos))
                sender.send(locked_repos)
                lock.release()
                logger.debug(repo_name+" is sending the ack")
                ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("ERROR: "+str(e))
        print("Message: "+str(body))
        logger.debug("dERROR: "+str(e))
        logger.debug("dMessage: "+str(body))
        logger.error("ERROR: "+str(e))
        logger.error("Message: "+str(body))

# def callback(ch, method, properties, body):
#     """
#     Consume messages from the ready queue
#     :param ch:
#     :param method:
#     :param properties:
#     :param body:
#     :return:
#     """
#     print("properties: ")
#     print(properties)
#     print("body: ")
#     print(body)
#     lock = properties['lock']
#     logger = properties['logger']
#     receiver = properties['receiver']
#     sender = properties['sender']
#
#     try:
#         print("properties: "+str(properties))
#         j = json.loads(body)
#         if j['action'] in ['magic', 'change_conf', 'publish']:
#             repo_name = j['repo']
#             #logger.debug('callback repo: '+repo_name)
#             lock.acquire()
#             locked_repos = receiver.recv()
#             busy = repo_name in locked_repos
#             if not busy:
#                 logger.debug('not busy repo: ' + repo_name + " (" + str(method.delivery_tag) + ")")
#                 locked_repos.append(repo_name)
#                 logger.debug("start locked repos: "+str(locked_repos))
#             else:
#                 logger.debug('is busy repo: ' + repo_name + " (" + str(method.delivery_tag) + ")")
#                 #logger.debug("busy ones: "+str(locked_repos))
#             sender.send(locked_repos)
#             lock.release()
#             if busy:
#                 #logger.debug(repo_name+" is busy --- ")
#                 time.sleep(5)
#                 ch.basic_nack(delivery_tag=method.delivery_tag, multiple=False, requeue=True)
#             else:
#                 logger.debug(" ---  Consuming: " + repo_name + "\n" + str(body))
#                 # logger.debug(body)
#                 if j['action'] == 'magic':
#                     logger.debug('starting a magic process')
#                     # p = Process(target=handle_action, args=(j, logger))
#                     # p.start()
#                     # p.join()
#                     handle_action(j, logger)
#                 elif j['action'] == 'change_conf':
#                     logger.debug('starting a config change process')
#                     # p = Process(target=handle_conf_change, args=(j, logger))
#                     # p.start()
#                     # p.join()
#                     handle_conf_change(j, logger)
#                 elif j['action'] == 'publish':
#                     logger.debug('starting a publish process')
#                     # p = Process(target=handle_publish, args=(j, logger))
#                     # p.start()
#                     # p.join()
#                     handle_publish(j, logger)
#                 else:
#                     logger.debug("starting nothing")
#                 logger.debug(repo_name+" Completed!")
#                 lock.acquire()
#                 locked_repos = receiver.recv()
#                 logger.debug(repo_name+" to remove it from locked repos")
#                 locked_repos.remove(repo_name)
#                 logger.debug(repo_name+" is removed")
#                 logger.debug("locked repos: ")
#                 logger.debug(str(locked_repos))
#                 sender.send(locked_repos)
#                 lock.release()
#                 logger.debug(repo_name+" is sending the ack")
#                 ch.basic_ack(delivery_tag=method.delivery_tag)
#
#     except Exception as e:
#         print("ERROR: "+str(e))
#         print("Message: "+str(body))
#         logger.debug("dERROR: "+str(e))
#         logger.debug("dMessage: "+str(body))
#         logger.error("ERROR: "+str(e))
#         logger.error("Message: "+str(body))


def handle_publish(j, logger):
    """
    :param j:
    :param logger: logger
    :return:
    """
    try:
        logger.debug("try publish")
        import autoncore
        autoncore.django_setup_script()
        print("set logger")
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
    except Exception as e:
        err = "Error in handle_publish"
        print(err)
        logger.debug(err)
        logger.error(err)
        err = str(e)
        print(err)
        logger.debug(err)
        logger.error(err)


def handle_action(j, logger):
    """
    :param j:
    :return:
    """
    try:
        logger.debug("try action")
        import autoncore
        autoncore.django_setup_script()

        print("set logger")
        logger.debug("handle_action> ")
        repo = j['repo']
        if j['action'] == 'magic':
            logger.debug("going for magic: "+str(j))
            try:
                autoncore.git_magic(j['repo'], j['useremail'], j['changedfiles'])
                logger.debug("magic success")
            except Exception as e:
                logger.debug("dException in magic")
                logger.debug("dException in magic for repo: "+j['repo'])
                logger.debug(str(e))
                logger.error("Exception in magic for repo: "+j['repo'])
                logger.error(str(e))
                print("Exception in magic for repo: "+j['repo'])
                print(str(e))
            logger.debug("magic is done")
        else:
            logger.debug("dInvalid magic redirect: ")
            logger.debug("dInvalid magic redirect with j: "+str(j))
            logger.error("Invalid magic redirect: ")
            logger.error("Invalid magic redirect with j: "+str(j))
    except Exception as e:
        logger.debug("dException 2 ")
        logger.debug("dException 2 for magic: "+str(e))
        logger.debug("dException for j: "+str(j))
        logger.error("Exception 2 ")
        logger.error("Exception 2 for magic: "+str(e))
        logger.error("Exception for j: "+str(j))

    logger.debug("finished handle_action: "+str(j))


def handle_conf_change(j, logger):
    """
    :param j:
    :param logger: logger
    :return:
    """
    try:
        logger.debug("try change")
        import autoncore
        autoncore.django_setup_script()
        print("set logger")
        logger.debug("handle_conf_change> ")
        data = j['data']
        if j['action'] == 'change_conf':
            autoncore.change_configuration(user_email=j['useremail'],
                                           target_repo=j['repo'], data=data, ontologies=j['ontologies'])
            logger.debug("handle_conf_change> configuration is changed: "+str(j))
        else:
            logger.debug("handle_conf_change> invalid action: "+str(j))
    except Exception as e:
        err = "Error in handle_conf_change"
        print(err)
        logger.debug(err)
        logger.error(err)
        err = str(e)
        print(err)
        logger.debug(err)
        logger.error(err)

    logger.debug("finished handle_conf_change: "+str(j))

# def handle_conf_change(j, logger):
#     """
#     :param j:
#     :param logger: logger
#     :return:
#     """
#     try:
#         logger.debug("try change")
#         import autoncore
#         from models import *
#         print("set logger")
#         logger.debug("handle_conf_change> ")
#         data = j['data']
#         if j['action'] == 'change_conf':
#             repo_name = j['repo'].strip()
#             repos = Repo.objects.filter(url=repo_name)
#             users = OUser.objects.filter(email=j['useremail'])
#             if len(repos) == 1:
#                 repo = repos[0]
#             else:
#                 logger.debug("handle_conf_change> Invalid repo: "+repo_name)
#                 raise Exception("Invalid repo: "+repo_name)
#             if len(users) == 1:
#                 user = users[0]
#             else:
#                 logger.debug("handle_conf_change> Invalid email: "+j['useremail'])
#                 raise Exception("Invalid email: "+j['useremail'])
#
#             orun = ORun(task='Change Configuration', user=user, repo=repo, description='Change configuration')
#             orun.save()
#             for onto in j['ontologies']:
#                 logger.debug('inside the loop')
#                 ar2dtool = onto + '-ar2dtool' in data
#                 # logger.debug('ar2dtool: ' + str(ar2dtool))
#                 widoco = onto + '-widoco' in data
#                 # print 'widoco: ' + str(widoco)
#                 oops = onto + '-oops' in data
#                 # logger.debug('oops: ' + str(oops)
#                 logger.debug('will call get_conf')
#                 orun.description += '. Get new configuration for the ontology: '+onto
#                 orun.save()
#                 new_conf = autoncore.get_conf(ar2dtool, widoco, oops)
#                 logger.debug('will call update_file')
#                 o = 'OnToology' + onto + '/OnToology.cfg'
#                 try:
#                     logger.debug("target_repo <%s> ,  path <%s> ,  message <%s> ,   content <%s>" % (
#                         j['repo'], o, 'OnToology Configuration', new_conf))
#                     orun.description += '. Update the configuration for the ontology: ' + onto
#                     orun.save()
#                     autoncore.update_file(j['repo'], o, 'OnToology Configuration', new_conf)
#                     logger.debug('configuration is changed for file for ontology: '+onto)
#                 except Exception as e:
#                     logger.error('Error in updating the configuration: ' + str(e))
#                     # return render(request, 'msg.html', {'msg': str(e)})
#                     return
#             orun.description += '. The task is completed successfully'
#             orun.save()
#             logger.debug('Configuration changed')
#     except Exception as e:
#         err = "Error in handle_conf_change"
#         print(err)
#         logger.debug(err)
#         logger.error(err)
#         err = str(e)
#         print(err)
#         logger.debug(err)
#         logger.error(err)
#
#     logger.debug("finished handle_conf_change: "+str(j))


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


def start_pool(num_of_processes=1):
    """
    :param num_of_processes:
    :return:
    """
    global logger
    processes = []
    lock = Lock()
    sender, receiver = Pipe()
    sender.send([])
    for i in range(num_of_processes):
        th = Process(target=single_worker, args=(i, lock, sender, receiver, logger))
        th.start()
        logger.debug("spawn: "+str(i))
        processes.append(th)
    logger.debug("total spawned: "+str(processes))
    for idx, th in enumerate(processes):
        th.join()
        logger.info("Process is closed: "+str(idx))
    logger.error("ALL ARE CONSUMED ..")


def single_worker(worker_id, lock, sender, receiver, logger):
    """
    :param worker_id:
    :return:
    """
    logger.debug('worker_id: '+str(worker_id))
    # heartbeat=0 disable timeout
    # heartbeat= 60 * 60 * 3 (3 hours)
    # connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host, heartbeat=0))
    worker_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
    channel = worker_connection.channel()
    queue = channel.queue_declare(queue=queue_name, durable=True, auto_delete=False)
    channel.basic_qos(prefetch_count=1)

    # while True:
    # channel.basic_get(queue=queue_name, auto_ack=False)
    # time.sleep(5)
    # channel.basic_consume(queue=queue_name, on_message_callback=callback, arguments={
    #     # 'lock': lock,
    #     # 'sender': sender,
    #     # 'reciever': reciever,
    #     # 'logger': logger
    # })

    abc = {
            'lock': lock,
            'sender': sender,
            'receiver': receiver,
            'logger': logger
    }
    abc_callback = partial(callback2, abc)
    channel.basic_consume(queue=queue_name, on_message_callback=abc_callback)
    print("Rabbit consuming is started ... "+str(worker_id))
    logger.debug("Setting the logger ..."+str(worker_id))
    logger.debug("test connection ..."+str(channel.is_open))
    logger.debug("single_worker> number of messages in the queue is: " + str(queue.method.message_count))
    channel.start_consuming()


if __name__ == '__main__':
    print("In rabbit\n\n")
    import autoncore
    if len(sys.argv) > 1:
        start_pool(int(sys.argv[1]))
    else:
        start_pool()

