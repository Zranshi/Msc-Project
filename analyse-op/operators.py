import itertools

import numpy as np

DB: dict[str, "Operator"] = {}


def arr_2_str(arr: np.ndarray):
    return " ".join(str(item) for item in arr.reshape(9))


class Operator:
    def __init__(
        self, idx: int, tt: int, tm: int, tf: int, mt: int, mm: int, mf: int, ft: int, fm: int, ff: int, count: int
    ) -> None:
        self.idx = idx
        self.arr: np.ndarray = np.array(
            [
                [tt, tm, tf],
                [mt, mm, mf],
                [ft, fm, ff],
            ]
        )
        self.count = count

    @classmethod
    def by_str(cls, s: str) -> "Operator":
        return DB[s]

    @classmethod
    def by_array(cls, arr: np.ndarray) -> "Operator":
        return DB[arr_2_str(arr)]

    def __str__(self) -> str:
        return arr_2_str(self.arr)

    def __repr__(self) -> str:
        return str(self.arr)

    def get_similar_operators(self):
        order = [0, 1, 2]
        for new_order in itertools.permutations(order):
            new_arr = self.arr.copy()
            for i in range(3):
                for j in range(3):
                    new_arr[i, j] = new_order[order.index(self.arr[i, j])]
            new_arr[new_order, :] = new_arr[order, :]
            new_arr[:, new_order] = new_arr[:, order]
            new_op = DB[arr_2_str(new_arr)]
            yield new_op

    @classmethod
    def get_symmetry_operator(cls):
        domin = [0, 1, 2]
        for item in itertools.product(*[domin for _ in range(6)]):
            arr = np.array(
                [
                    [item[0], item[1], item[3]],
                    [item[1], item[2], item[4]],
                    [item[3], item[4], item[5]],
                ]
            )
            yield Operator.by_array(arr)

    @classmethod
    def filter_similar_operator(
        cls, ops: list["Operator"], pre_sort: bool = True, post_sort: bool = True
    ) -> list["Operator"]:
        op_set: set[Operator] = set()
        if pre_sort:
            ops.sort(key=lambda item: str(item))
        for op in ops:
            if all([item not in op_set for item in op.get_similar_operators()]):
                op_set.add(op)
        result = list(op_set)
        if post_sort:
            result.sort(key=lambda item: str(item))
        return result


with open("../find-op/output", "r") as f:
    for line in f.readlines():
        idx, string, count = line.split(",")
        idx = int(idx)
        mapping = [int(item) for item in string.split(" ")]
        count = int(count)
        DB[string] = Operator(idx, *mapping, count)
