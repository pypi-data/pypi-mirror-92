import numpy as np


class KGLPMetrics:
    def __init__(self):
        self._hits_1 = 0.0
        self._hits_5 = 0.0
        self._hits_10 = 0.0
        self.count = 0.0
        self._mrr = 0.0
        self.ranks = list()

    @property
    def hits_at_1(self):
        if self.count == 0:
            return 0.0
        return self._hits_1 / self.count

    @property
    def hits_at_5(self):
        if self.count == 0:
            return 0.0
        return self._hits_5 / self.count

    @property
    def hits_at_10(self):
        if self.count == 0:
            return 0.0
        return self._hits_10 / self.count

    @property
    def mrr(self):
        if self.count == 0:
            return 0.0
        return self._mrr / self.count

    def zeros(self):
        self._hits_1 = 0.0
        self._hits_5 = 0.0
        self._hits_10 = 0.0
        self.count = 0.0
        self._mrr = 0.0

    def clear(self):
        self.zeros()

    def copy(self):
        result = KGLPMetrics()
        result._hits_1 = self._hits_1
        result._hits_5 = self._hits_5
        result._hits_10 = self._hits_10
        result._mrr = self._mrr
        result.count = self.count
        result.ranks = self.ranks[:]
        return result

    @property
    def raw(self) -> str:
        result = dict()
        result['hits@1'] = self._hits_1
        result['hits@5'] = self._hits_5
        result['hits@10'] = self._hits_10
        result['count'] = self.count
        result['mrr'] = self._mrr
        result['ranks'] = self.ranks
        return str(result)

    def __str__(self):
        result = dict()
        result['Hits@1'] = f"{self.hits_at_1:.3f}"
        result['Hits@5'] = f"{self.hits_at_5:.3f}"
        result['Hits@10'] = f"{self.hits_at_10:.3f}"
        result['MRR'] = f"{self.mrr:.3f}"
        return str(result)

    def __add__(self, other):
        if isinstance(other, KGLPMetrics):
            result = self.copy()
            result._hits_1 += other._hits_1
            result._hits_5 += other._hits_5
            result._hits_10 += other._hits_10
            result.count += other.count
            result._mrr += other._mrr
            result.ranks.extend(other.ranks)
            return result
        else:
            raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, KGLPMetrics):
            return self.mrr > other.mrr
        else:
            raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, KGLPMetrics):
            return self.mrr == other.mrr
        else:
            raise NotImplementedError

    def update(self, rank: int):
        self.ranks.append(rank)
        self.count += 1
        self._mrr += 1.0 / rank
        if rank <= 1:
            self._hits_1 += 1
            self._hits_10 += 1
            self._hits_5 += 1
        elif rank <= 5:
            self._hits_5 += 1
            self._hits_10 += 1
        elif rank <= 10:
            self._hits_10 += 1
        else:
            return


def perform_metrics(scores: np.ndarray, golden_idx: int = 0) -> KGLPMetrics:
    """

    :param scores: shape (Q,)
    :param golden_idx: the true index, default is 0
    :return:
    """
    result = KGLPMetrics()
    sort = list(np.argsort(scores, kind='stable'))[::-1]  # reverse a list
    rank = sort.index(golden_idx) + 1
    result.update(rank)
    return result
