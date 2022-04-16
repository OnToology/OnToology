from stiqueue.sqserver import SQServer
import traceback
import os
import sys
from multiprocessing import Lock
import logging
import json
try:
    from localwsgi import *
except:
    pass


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
    logger.handlers = []
    # while len(logger.handlers) > 0:#logger.hasHandlers():
    #     logger.removeHandler(logger.handlers[0])
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


class SQServer2(SQServer):
    def other_actions(self, action_msg):
        action = action_msg[:self.action_len]
        if len(action_msg) >= self.action_len:
            msg = action_msg[self.action_len:]
            if action == b"enm":
                if self.debug:
                    self.logger.debug("SERVER> enqueue: ")
                    self.logger.debug(msg)
                self.lock.acquire()
                txt = msg.decode()
                j = json.loads(txt)
                try:
                    merged = False
                    for req in self.q:
                        if req['repo'] == j['repo'] and req['action'] == j['action']:
                            if j['action'] == 'magic':
                                if j['branch'] == req['branch']:
                                    merged = True
                                    print("Merged: <<%s>> with <<%s>>" % (str(req), str(j)))
                                    req['changedfiles'] += j['changedfiles']
                                    req['changedfiles'] = list(set(req['changedfiles']))
                            if j['action'] == 'publish':
                                if j['ontology_rel_path'] == req['ontology_rel_path'] and j['branch'] == req['branch']:
                                    merged = True
                                    print("Merged: <<%s>> with <<%s>>" % (str(req), str(j)))
                                    # There is already a request to publish, no need to add another one
                    if not merged:
                        self.q.append(txt)
                except Excepion as e:
                    print("Exception: %s" % str(e))
                    traceback.print_exc()
                self.lock.release()
            else:
                print("ERROR: invalid action:")
                print(action_msg)
                print(action)
        else:
            print("Error: invalid action length:")
            print(action_msg)
            print(action)


if __name__ == '__main__':
    debug = False
    logger = None
    if 'stiq_debug' in os.environ:
        if os.environ['stiq_debug'].lower() == "true":
            debug = True
            print("SERVER> Debug is on")
            logger = logging.getLogger(__name__)
            logger_path = ""
            if 'stiq_server_log_path' in os.environ:
                logger_path = os.environ['stiq_server_log_path']
                print("logger: %s" % logger_path)
            else:
                print("logger is not here: ")
                print(os.environ)
            logger = set_config(logger, logger_path)
    if len(sys.argv) > 2:
        s = SQServer2(sys.argv[1], int(sys.argv[2]), str_queue=True, debug=debug, logger=logger)
    else:
        if "stiq_host" in os.environ and "stiq_port" in os.environ:
            s = SQServer2(host=os.environ['stiq_host'], port=int(os.environ['stiq_port']), str_queue=True, debug=debug,
                          logger=logger)
        else:
            s = SQServer2(debug=debug, str_queue=True, logger=logger)
    s.listen()




