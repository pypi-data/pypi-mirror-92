import pandas as pd
from conf.configuration import *
import logging
def parts(dataset,separator=","):
    part_count_dateset= get_part_count(dataset)
    logging.warning("iterating over the parts of %s"%dataset)
    for part in range(part_count_dateset):
        path=get_path_preprocessed_documents_version(dataset,str(part))
        df_part=pd.read_csv(path,sep=separator,quotechar='"',encoding="utf-8")
        logging.warning("part %d is read"%part)
        yield df_part
