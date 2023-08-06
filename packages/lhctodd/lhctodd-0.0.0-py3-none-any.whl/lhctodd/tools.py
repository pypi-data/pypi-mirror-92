import numpy as np
import os
from pathlib import Path

class dd_format:
    def __init__(self, limit, meta):
        self.ncol = limit.shape[1]
        self.size = limit.shape[0]

        self.limit = limit.tobytes()
        self.cite = meta.get("cite", "None")
        self.year = meta.get("year", "None")
        self.type = meta.get("type", "None")
        self.expr = meta.get("expr", "None")
        self.name = meta.get("name", "None")

    def get_limit(self):
        limit = np.frombuffer(self.limit, dtype=np.float64)
        return limit.reshape(self.size, self.ncol)

    def __str__(self):
        return "https://arxiv.org/abs/{0} {1} {2}".format(self.cite, self.type, self.name)


__data_path__ = Path(os.path.join(os.path.dirname(__file__), "data"))
