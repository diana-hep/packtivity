import logging
from packtivity.utils import mkdir_p


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# class TopicLogger(object):
#     def __init__(self,basepath):
#         self.basepath = basepath
#         self.parentname = 'packtivity_logger'
#         self.logger = logging.getLogger(self.parentname)
#         self.logger.setLevel(logging.DEBUG)

#         fh  = logging.StreamHandler()
#         fh.setLevel(logging.INFO)
#         fh.setFormatter(formatter)
#         self.logger.addHandler(fh)

#     def topic(self,topic):
#         l = logging.getLogger('.'.join([self.parentname,topic]))
#         l.setLevel(logging.DEBUG)
#         if not l.handlers:
#             fh = logging.FileHandler(os.path.join(self.basepath,'pack.{}.log'.format(topic)))
#             fh.setFormatter(formatter)
#             fh.setLevel(logging.DEBUG)
#             l.addHandler(fh)
#         return l

def get_base_loggername(nametag):
    return 'packtivity_logger_{}'.format(nametag)

def get_topic_loggername(nametag,topic):
    return 'packtivity_logger_{}.{}'.format(nametag,topic)

def setup_logging(nametag,context):
    ## prepare logging for the execution of the job. We're ready to handle up to DEBUG
    log = logging.getLogger(get_base_loggername(nametag))
    log.setLevel(logging.DEBUG)

    fh  = logging.StreamHandler()
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    ## this is all internal logging, we don't want to escalate to handlers of parent loggers
    ## we will have two handlers, a stream handler logging to stdout at INFO
    log.propagate = False
    setup_logging_topic(nametag,context,'step')

def setup_logging_topic(nametag,context,topic, return_logger = False):
    log = logging.getLogger(get_topic_loggername(nametag,topic))
    log.propagate = False

    if topic == 'step':
        fh  = logging.StreamHandler()
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    # short interruption to create metainfo storage location
    metadir  = '{}/_packtivity'.format(context['readwrite'][0])
    context['metadir'] = metadir
    # log.info('creating metadirectory %s if necessary. exists? : %s',metadir,os.path.exists(metadir))
    mkdir_p(metadir)

    # Now that we have  place to store meta information we put a file based logger in place
    # to log at DEBUG
    logname = '{}/{}.{}.log'.format(metadir,nametag,topic)
    fh  = logging.FileHandler(logname)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    if return_logger:
        return log
