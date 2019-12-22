# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import dill
import random
import numpy as np


class SearchSpace:
    def __init__(self, _core_, model_nr):
        self.search_space = _core_.search_config[list(_core_.search_config)[model_nr]]
        self.pos_space_limit()
        self.init_type = None

        if _core_.init_config:
            self.init_para = _core_.init_config[list(_core_.init_config)[model_nr]]

            if list(self.init_para.keys())[0] == list(self.search_space.keys())[0]:
                self.init_type = "warm_start"
            elif list(self.init_para.keys())[0] == "scatter_init":
                self.init_type = "scatter_init"

    def pos_space_limit(self):
        dim = []

        for pos_key in self.search_space:
            dim.append(len(self.search_space[pos_key]) - 1)

        self.dim = np.array(dim)

    def get_random_pos(self):
        pos_new = np.random.uniform(np.zeros(self.dim.shape), self.dim, self.dim.shape)
        pos = np.rint(pos_new).astype(int)

        return pos

    def get_random_pos_scalar(self, hyperpara_name):
        n_para_values = len(self.search_space[hyperpara_name])
        pos = random.randint(0, n_para_values - 1)

        return pos

    def _read_dill(self, value, path):
        with open(path, "rb") as fp:
            value = dill.load(fp)
            value = dill.loads(value)

        return value

    def para2pos(self, para, _get_pkl_hash):
        pos_list = []

        for pos_key in self.search_space:
            value = para[[pos_key]].values[0][0]

            if isinstance(value, str):

                if len(value) == 40:
                    paths = _get_pkl_hash(value)
                    for path in paths:
                        value = self._read_dill(value, path)

                        if not isinstance(value, str):
                            break

            pos = self.search_space[pos_key].index(value)
            pos_list.append(pos)

        return np.array(pos_list)

    def pos2para(self, pos):
        if len(self.search_space.keys()) == pos.size:
            values_dict = {}
            for i, key in enumerate(self.search_space.keys()):
                pos_ = int(pos[i])
                values_dict[key] = list(self.search_space[key])[pos_]

            return values_dict
