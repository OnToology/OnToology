import json
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
from threading import Lock
from multiprocessing import Process, Pipe
import multiprocessing
import traceback

from stiqueue.sqclient import SQClient


locked_repos = []
lock = Lock()

host = "127.0.0.1"
port = 1234


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


if 'stiq_host' in os.environ:
    host = os.environ['stiq_host']
if 'stiq_port' in os.environ:
    port = int(os.environ['stiq_port'])


if 'stiq_log_dir' in os.environ:
    log_dir = os.environ['stiq_log_dir']
    logger = multiprocessing.get_logger()
    logger = set_config(logger, log_dir)
else:
    logger = multiprocessing.get_logger()
    logger = set_config(logger)


def client_loop(host, port):
    print("client_loop: %s %d" % (host, port))
    cc = SQClient(host=host, port=port)
    while True:
        time.sleep(1)
        # print(b"CLIENT> get num ")
        v = cc.deq()
        if v == b"":
            continue
        body = v.decode()
        print("CLIENT: Getting value: %s" % body)
        if can_proceed(body):
            print("body: %s" % body)
            th = threading.Thread(target=consume, args=(body,))
        else:
            th = threading.Thread(target=send_with_delay, args=(cc, v, 10))
        th.start()


def send_with_delay(client, data_bytes, delay):
    time.sleep(delay)
    client.enq(data_bytes)



# queue_name = 'ontoology'
#
# print("Will check the rabbit host \n\n\n")
# if 'rabbit_host' in os.environ:
#     rabbit_host = os.environ['rabbit_host']
#     print("rabbit_host: "+rabbit_host)
# else:
#     rabbit_host = 'localhost'
#     print("rabbit_host: "+rabbit_host)
#
# if 'rabbit_log_dir' in os.environ:
#     log_dir = os.environ['rabbit_log_dir']
#     logger = multiprocessing.get_logger()
#     # logger = logging.getLogger(__name__)
#     logger = set_config(logger, log_dir)
# else:
#     # logger = logging.getLogger(__name__)
#     logger = multiprocessing.get_logger()
#     logger = set_config(logger)


# def run_rabbit():
#     """
#     Run the rabbit consumer
#     :return:
#     """
#     pass
#     # if 'rabbit_processes' in os.environ:
#     #     try:
#     #         num = int(os.environ['rabbit_processes'])
#     #         if 'virtual_env_dir' in os.environ:
#     #             comm = "nohup %s %s %s %s" % (os.path.join(os.environ['virtual_env_dir'], 'bin', 'python'),
#     #                                           os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rabbit.py'),
#     #                                           str(num), os.environ['setting_module'], ' &')
#     #         else:
#     #             comm = "nohup python %s %s %s" % (
#     #             os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rabbit.py'), str(num), '&')
#     #         logger.debug("run_rabbit> comm: " + comm)
#     #         print("run_rabbit> comm: " + comm)
#     #         subprocess.Popen(comm, shell=True)
#     #     except:
#     #         logger.error('run_rabbit> The rabbit_processes is: <%s>' % str(os.environ['rabbit_processes']))
#     # else:
#     #     logger.debug('run_rabbit> rabbit_processes is not in environ')


def send(message_json):
    """
    :param message_json: dict
    :return:
        None
    """
    # global logger
    message = json.dumps(message_json)
    # logger.debug("send> sending message: "+str(message))
    print("Sending: ")
    print(message)
    c = SQClient(host=host, port=port)
    c.enq(str.encode(message))


def get_pending_messages():
    """
    get number of pending messages
    :return:
    """
    print("sqclient> get_pending_messages> %s %d" % (host, port))
    c = SQClient(host=host, port=port)
    num = int(c.cnt())
    print("SQClient> get_pending_messages> Number of elements in the queue are: %d" % num)
    return num


# def get_num_of_processes_of_rabbit():
#     """
#     :return:
#     """
#     import os
#     out = os.popen('ps -ef | grep rabbit.py').read()
#     lines = out.split('\n')
#     one = False
#     for line in lines:
#         if 'python' in line and 'rabbit.py' in line:
#             print("line: ")
#             print(line)
#             p_tokens = line.split('rabbit.py')
#             if len(p_tokens) > 1:
#                 tokens = p_tokens[1].strip().split(' ')
#                 if tokens[0].strip().isdigit():
#                     return int(tokens[0].strip())
#                 else:
#                     print("ptokens: ")
#                     print(p_tokens)
#                     print("tokens: ")
#                     print(tokens)
#                     # return 1
#                     one = True
#     if one:
#         return 1
#     return -1


# def direct_call(j):
#     """
#     Consume messages from the ready queue
#     :param j:
#     :return:
#     """
#     global logger
#     try:
#         if j['action'] in ['magic', 'change_conf', 'publish']:
#             repo_name = j['repo']
#             logger.debug(" ---  Consuming: " + repo_name + "\n" + str(j))
#             if j['action'] == 'magic':
#                 logger.debug('starting a magic process')
#                 handle_action(j, logger)
#             elif j['action'] == 'change_conf':
#                 logger.debug('starting a config change process')
#                 handle_conf_change(j, logger)
#             elif j['action'] == 'publish':
#                 logger.debug('starting a publish process')
#                 handle_publish(j, logger)
#             else:
#                 logger.debug("starting nothing")
#             logger.debug(repo_name+" Completed!")
#             return True
#
#     except Exception as e:
#         print("ERROR: "+str(e))
#         print("Message: "+str(j))
#         logger.debug("dERROR: "+str(e))
#         logger.debug("dMessage: "+str(j))
#         logger.error("ERROR: "+str(e))
#         logger.error("Message: "+str(j))
#         return False


def consume(body):
    """
    Consume the request.

    body: json string.

    """
    j = json.loads(body)
    repo_name = j['repo']
    logger.debug(" ---  Consuming: " + repo_name + "\n" + str(j))
    if j['action'] == 'magic':
        logger.debug('starting a magic process')
        handle_action(j, logger)
    elif j['action'] == 'change_conf':
        logger.debug('starting a config change process')
        handle_conf_change(j, logger)
    elif j['action'] == 'publish':
        logger.debug('starting a publish process')
        handle_publish(j, logger)
    else:
        logger.debug("starting nothing")
    logger.debug(repo_name + " Completed!")
    lock.acquire()
    logger.debug(repo_name + " to remove it from locked repos")
    logger.debug("locked repos: %s" % str(locked_repos))
    locked_repos.remove(repo_name)
    logger.debug(repo_name + " is removed")
    logger.debug("locked repos: ")
    logger.debug(str(locked_repos))
    lock.release()


def can_proceed(body):
    """
    Consume messages from the ready queue
    :param body:
    :return: bool
    """

    j = json.loads(body)
    if j['action'] in ['magic', 'change_conf', 'publish']:
        repo_name = j['repo']
        lock.acquire()
        busy = repo_name in locked_repos
        if not busy:
            repo_pure_name = repo_name.split('/')[1]
            pure_locked = [r.split('/')[1] for r in locked_repos]
            pure_busy = repo_pure_name in pure_locked
        else:
            pure_busy = busy
        if not pure_busy:
            logger.debug('not busy repo: ' + repo_name)
            locked_repos.append(repo_name)
            logger.debug("start locked repos: "+str(locked_repos))
        else:
            logger.debug('is busy repo: ' + repo_name)
        # sender.send(locked_repos)
        lock.release()
        return not pure_busy
    #         # if busy:
    #         #     #logger.debug(repo_name+" is busy --- ")
    #         #     time.sleep(5)
    #         #     # ch.basic_nack(delivery_tag=method.delivery_tag, multiple=False, requeue=True)
    #         # else:
    #         #     p = Process(target=callback_consumer, args=(lock, sender, receiver, logger, j))
    #         #     p.start()
    #         #     ch.basic_ack(delivery_tag=method.delivery_tag)
    #
    # except Exception as e:
    #     print("ERROR: "+str(e))
    #     print("Message: "+str(body))
    #     logger.debug("dERROR: "+str(e))
    #     logger.debug("dMessage: "+str(body))
    #     logger.error("ERROR: "+str(e))
    #     logger.error("Message: "+str(body))
    #


def handle_publish(j, logger):
    """
    :param j:
    :param logger: logger
    :return:
    """
    try:
        logger.debug("try publish")
        try:
            import autoncore
            autoncore.django_setup_script()
        except:
            from OnToology import autoncore
        print("set logger")
        logger.debug('handle_publish> going for previsual')
        try:
            err, orun = autoncore.previsual(useremail=j['useremail'], target_repo=j['repo'], branch=j['branch'])
            logger.debug("handle_publish> prev error: %s" % str(err))
        except Exception as e:
            logger.debug('handle_publish> Error in previsualisation')
            logger.error('handle_publish> ERROR in previsualisation: '+str(e))
            return
        if err.strip() != "":
            logger.debug('handle_publish> Error in previsual and will stop')
            return
        logger.debug('handle_publish> going for publish')
        try:
            autoncore.publish(name=j['name'], target_repo=j['repo'], ontology_rel_path=j['ontology_rel_path'],
                              useremail=j['useremail'], branch=j['branch'], orun=orun)
        except Exception as e:
            traceback.print_exc()
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


def handle_action(j, logger, raise_exp=False):
    """
    :param j:
    :return:
    """
    try:
        logger.debug("try action")
        try:
            import autoncore
            autoncore.django_setup_script()
        except:
            from OnToology import autoncore

        print("set logger")
        logger.debug("handle_action> ")
        repo = j['repo']
        if j['action'] == 'magic':
            logger.debug("going for magic: "+str(j))
            try:
                autoncore.git_magic(j['repo'], j['useremail'], j['changedfiles'], j['branch'], raise_exp=raise_exp)
                logger.debug("magic success")
            except Exception as e:
                logger.debug("dException in magic")
                logger.debug("dException in magic for repo: "+j['repo'])
                logger.debug(str(e))
                logger.error("Exception in magic for repo: "+j['repo'])
                logger.error(str(e))
                print("Exception in magic for repo: "+j['repo'])
                print(str(e))
                traceback.print_exc()
                if raise_exp:
                    raise Exception(str(e))
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
        traceback.print_exc()
        if raise_exp:
            raise Exception(str(e))
    logger.debug("finished handle_action: "+str(j))


def handle_conf_change(j, logger):
    """
    :param j:
    :param logger: logger
    :return:
    """
    try:
        logger.debug("try change")
        try:
            import autoncore
            autoncore.django_setup_script()
        except:
            from OnToology import autoncore
        print("set logger")
        logger.debug("handle_conf_change> ")
        data = j['data']
        if j['action'] == 'change_conf':
            autoncore.change_configuration(user_email=j['useremail'], target_repo=j['repo'], data=data,
                                           ontologies=j['ontologies'])
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


# if __name__ == '__main__':
#     print("In rabbit\n\n")
#     if len(sys.argv) > 1:
#         start_pool(int(sys.argv[1]))
#         if len(sys.argv) > 2:
#             from .djangoperpmodfunc import load
#             load(sys.argv[2])
#             import autoncore
#             from .localwsgi import *
#             print("\n\nrabbit __main__: .........................environ:")
#             print(environ)
#     else:
#         start_pool()


if __name__ == "__main__":
    print("CLIENT started")
    from djangoperpmodfunc import load
    if len(sys.argv) == 1:
        load("OnToology.settings")
    else:
        print("load settings: %s" % sys.argv[1])
        load(sys.argv[1])

    import os

    if 'stiq_host' in os.environ:
        host = os.environ['stiq_host']
    if 'stiq_port' in os.environ:
        port = int(os.environ['stiq_port'])

    if 'stiq_log_dir' in os.environ:
        log_dir = os.environ['stiq_log_dir']
        logger = multiprocessing.get_logger()
        logger = set_config(logger, log_dir)
    else:
        logger = multiprocessing.get_logger()
        logger = set_config(logger)

    import autoncore
    from localwsgi import *
    from OnToology.models import *
    print(OUser.objects.all())
    print(Repo.objects.all())
    client_loop(host, port)

