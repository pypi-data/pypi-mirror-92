"""Top-level package for lhctodd."""

__author__ = """Yacine Haddad"""
__email__ = 'yhaddad@cern.ch'
__version__ = '0.1.0'

import os
import lmdb
import pickle
from pathlib import Path
from prettytable import PrettyTable

from . import theory
from .tools import dd_format
from .tools import __data_path__
from .model import DD
from .model import SI
from .model import SD

def list(search=None):
    env = lmdb.open(str(__data_path__ / f"darkmatter-data"), readonly=True)
    output = PrettyTable()
    output.field_names = ["id", "type", "Experiment", "arXiv"]
    with env.begin() as txn:
        for key, _ in txn.cursor():
            raw = txn.get(key)
            data = pickle.loads(raw)
            if search:
                if search in data.__dict__.values():
                    output.add_row([
                        int(key.decode()),
                        data.type,
                        data.expr,
                        data.cite
                    ])

            else:
                output.add_row([
                    int(key.decode()),
                    data.type,
                    data.expr,
                    data.cite
                ])
    env.close()
    print(output)


__all__ = ["model", "DD", "SI", "SD", "list"]
