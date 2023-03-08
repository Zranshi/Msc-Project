from collections import deque
from itertools import product


class Operator:
    def __init__(
        self,
        tt: int,
        tm: int,
        tf: int,
        mt: int,
        mm: int,
        mf: int,
        ft: int,
        fm: int,
        ff: int,
    ) -> None:
        self.cal_map = {
            (2, 2): tt,
            (2, 1): tm,
            (2, 0): tf,
            (1, 2): mt,
            (1, 1): mm,
            (1, 0): mf,
            (0, 2): ft,
            (0, 1): fm,
            (0, 0): ff,
        }

    def cal(self, formar: tuple, latter: tuple) -> tuple:
        res = []
        for i in range(9):
            res.append(self.cal_map[(formar[i], latter[i])])
        return tuple(res)

    def __str__(self) -> str:
        return f"{self.cal_map}"


def full_arrangement():
    domin = [0, 1, 2]
    for item in product(*[domin for _ in range(9)]):
        yield item


def check(op: Operator):
    s1 = (2, 2, 2, 1, 1, 1, 0, 0, 0)
    s2 = (2, 1, 0, 2, 1, 0, 2, 1, 0)
    d = {s1}
    new_que = deque([s2])
    while new_que:
        s = new_que.popleft()
        new: set[tuple] = set()
        res = op.cal(s, s)
        if res not in d:
            new.add(res)
        for t in d:
            res = op.cal(s, t)
            if res not in d:
                new.add(res)
            res = op.cal(t, s)
            if res not in d:
                new.add(res)
        for item in new:
            d.add(item)
            new_que.append(item)
    print(op, end=" | ")
    print(len(d))
    if len(d) == 3**9:
        print(op)


def main():
    idx = 0
    for v in full_arrangement():
        print(f"{idx} / {3**9}", end=" | ")
        check(Operator(*v))
        idx += 1


if __name__ == "__main__":
    main()
