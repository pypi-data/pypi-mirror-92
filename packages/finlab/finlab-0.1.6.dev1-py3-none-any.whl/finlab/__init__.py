import os
from .backtest import sim

__version__ = '0.1.6.dev1'

class Token:
    def __init__(self, interaction=True):

        if interaction and 'finlab_id_token' not in os.environ:
            id_token = input('Please login to https://finlab-python.github.io/finlab/ and copy api token here: \n')
            os.environ['finlab_id_token'] = id_token
        pass

    def set(self, token):
        os.environ['finlab_id_token'] = token

    def get(self):
        if 'finlab_id_token' in os.environ:
            return os.environ['finlab_id_token']
        else:
            return None
