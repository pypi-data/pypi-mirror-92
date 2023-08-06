import gc
import logging
import os
import random
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
from prettytable import PrettyTable


def get_logger():
    FORMAT = "[%(levelname)s]%(asctime)s:%(name)s:%(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    return logger


def timer(start_time=None):
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        tmin, tsec = divmod((datetime.now() - start_time).total_seconds(), 60)
        print(" Time taken: %i minutes and %s seconds." % (tmin, round(tsec, 2)))


def seed_everything(seed=2021):
    gc.enable()
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)

    warnings.filterwarnings('always')
    warnings.filterwarnings('ignore')
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)
    warnings.simplefilter(action='ignore', category=FutureWarning)

    pd.set_option('precision', 5)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('max_colwidth', -1)


def get_stage(value):
    bcolors = dict(HEADER='\033[95m',
                   OKBLUE='\033[94m',
                   OKGREEN='\033[90m',
                   WARNING='\033[93m',
                   FAIL='\033[91m',
                   ENDC='\033[0m',
                   BOLD='\033[1m',
                   UNDERLINE='\033[4m')

    if value == 0:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}::::::::::::DATASET ANALYSIS ::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 1:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}1.1 ::::::::::::DATASET ROWS  ::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 2:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}1.2 ::::::::::::DATASET VARIABLES ANALYSIS ::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 3:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}1.3 ::::::::::::DATASET RESUME ANALYSIS ::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 4:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")} ::::::::::::DATASET CLEANING ::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 5:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}2.1 ::::::::::::DATASET OUTLIER::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 6:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}2.1 ::::::::::::DATASET OUTLIER NUMERIC PROCESSING::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 7:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}2.2 ::::::::::::DATASET MISSING PROCESSING::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 8:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}2.2 ::::::::::::DATASET WOE PROCESSING::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 9:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}2.2 ::::::::::::DATASET BINDING PROCESSING::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 10:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}2.2 ::::::::::::DATASET CORRELATION PROCESSING::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 11:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")} ::::::::::::DATASET FEATURE SELECTION::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 12:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")}3.1 ::::::::::::DATASET COMPARE SELECTION::::::::::::{bcolors.get("ENDC")}']
        print(t)

    elif value == 13:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")} ::::::::::::DATASET MODEL BASELINE::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 14:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")} ::::::::::::DATASET PARAMETER MODEL::::::::::::{bcolors.get("ENDC")}']
        print(t)
    elif value == 15:
        t = PrettyTable()
        t.field_names = [f'{bcolors.get("OKGREEN")} ::::::::::::DATASET RUN MODEL::::::::::::{bcolors.get("ENDC")}']
        print(t)
