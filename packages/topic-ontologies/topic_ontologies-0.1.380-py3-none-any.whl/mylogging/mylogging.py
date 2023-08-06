import logging
from datetime import datetime
import random
def setup_logging(file):
    logging.basicConfig(format="%(message)s",filename=file,level=logging.DEBUG)
    logging.warning(datetime.now())
def log(message):
    logging.warning(message)

def log_status(counter,size,debug):
    percentage=(float(counter)/size)*100
    if debug and random.randint(0,100) %13 ==0:
        logging.warning("finished %2.2f"%percentage)

def log_matches(id,topic_id,debug):
    if debug and random.randint(0,100) %13 ==0:
        logging.warning("matched ontology topic id %s for %d"%(topic_id,id))
def log_size(dataset,size):
    logging.warning("size of %s is %d"%(dataset,size))