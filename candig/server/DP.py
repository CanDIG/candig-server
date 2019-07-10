from collections import defaultdict
import numpy as np


class DP(object):

    def __init__(self, federated_individuals, eps):
        self._servers = federated_individuals
        self._epsilon = {}
        for k, v in self._servers.items():
            self._epsilon[k] = eps

    def get_noise(self):
        federated_counts_dp = defaultdict()

        for k, v in self._servers.items():
            federated_counts_dp[k] = self._add_noise(v, k)

        return federated_counts_dp

    def _add_noise(self, vec, server, sensitivity=1.):

        if server not in self._epsilon:
            # print("Warning! Server has no registered privacy settings. Returning original results")
            return vec

        if self._epsilon[server] == np.inf:
            return vec

        scale = np.float64(sensitivity) / np.float64(self._epsilon[server])

        if type(vec) is dict:
            if not vec:
                # print("Warning! can't add noise to empty input");
                return vec
            for pop, v in vec.items():
                if type(v) is dict:
                    for var, count in v.items():
                        vec[pop][var] += int(np.random.laplace(0, scale=scale))
                        vec[pop][var] = max(vec[pop][var], 1)
                else:
                    vec[pop] += int(np.random.laplace(0, scale=scale))
                    vec[pop] = max(vec[pop], 1)
        else:
            vec += int(np.random.laplace(0, scale=scale))
            vec = max(vec, 1)
        return vec
