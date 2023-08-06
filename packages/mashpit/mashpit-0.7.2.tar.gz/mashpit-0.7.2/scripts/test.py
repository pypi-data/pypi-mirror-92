#!/usr/bin/env python3

import pickle
import threading
from sourmash import load_one_signature, load_signatures, save_signatures
from scripts.create_db import create_connection
from scripts.query_against_db import select_by_srr
import time


def load_sig(i):
        database_sig = load_signatures('outbreak_' + str(i) + '.sig')
        for sig in database_sig:
                pass


for i in range(1,7):
        thread = threading.Thread(target=load_sig, args=(i,))
        thread.start()