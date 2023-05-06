import numpy as np

from typing import Any, List, Tuple

class SumTree:
    write = 0

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)
        self.data = np.zeros(capacity, dtype=object)
        self.n_entries = 0

    def _propagate(self, idx, change):
        """update to the root node"""
        while (idx != 0).any():
            parent = (idx - 1) // 2
            np.add.at(self.tree, parent[idx != 0], change[idx != 0])
            idx = np.where(idx == 0, idx, parent)
        
    def _retrieve(self, idx, s):
        """find sample on leaf node"""
        while ((left := idx * 2 + 1) < len(self.tree)).any():
            right = left + 1

            left[left >= len(self.tree)] = idx[left >= len(self.tree)]
            right[right >= len(self.tree)] = idx[right >= len(self.tree)]
            idx = np.where(s <= self.tree[left], left, right)
            s = np.where(s <= self.tree[left], s, s - self.tree[left])
        return idx

    def total(self) -> float:
        for i in range(0, len(self.tree) // 2):
            np.allclose(self.tree[i], self.tree[2 * i + 1] + self.tree[2 * i + 2])
        return self.tree[0]

    def add(self, p: List[float], data: List[Any]):
        """store priority and sample"""
        idx = self.write +  np.arange(len(p))
        idx %= self.capacity
        idx += self.capacity - 1

        self.data[idx - self.capacity + 1] = data
        self.update(idx, p)

        self.write += len(p)
        self.n_entries = min(self.n_entries + len(p), self.capacity)

    def update(self, idx: List[int], p: List[float]):
        """update priority"""
        idx = np.array(idx).reshape(-1)
        p = np.array(p).reshape(-1)

        change = p - self.tree[idx]

        self.tree[idx] = p
        self._propagate(idx, change)

    def get(self, s: List[float], unique: bool = False) -> Tuple[List[int], List[float], List[Any]]:
        """get priority and sample"""
        idx = self._retrieve(np.zeros(s.shape, dtype=int), s)
        if unique:
            idx = np.unique(idx)
        dataIdx = idx - self.capacity + 1

        return (idx, self.tree[idx], self.data[dataIdx])