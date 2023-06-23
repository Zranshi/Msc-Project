from collections import deque
from functools import lru_cache
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

    @lru_cache(19683)
    def cal(self, formar: tuple, latter: tuple) -> tuple:
        return tuple([self.cal_map[(formar[i], latter[i])] for i in range(9)])

    def __str__(self) -> str:
        return f"{self.cal_map}"


def check(op: Operator):
    s1 = (2, 2, 2, 1, 1, 1, 0, 0, 0)
    s2 = (2, 1, 0, 2, 1, 0, 2, 1, 0)
    d = {s1, s2}
    new_que = deque([s1, s2])
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
        if len(d) == 19683:
            break
    return f"{op.cal_map}|{len(d)}"


def full_arrangement():
    domin = [0, 1, 2]
    for item in product(*[domin for _ in range(9)]):
        yield item


def main():
    idx = 0
    with open("./output", "w+") as f:
        for v in full_arrangement():
            print(f"{idx} / {3**9}", end=" | ")
            f.write(f"{idx}|{check(Operator(*v))}\n")
            idx += 1
            f.flush()
    # check(Operator(0, 1, 0, 0, 2, 2, 1, 0, 2))
    # check(Operator(1, 2, 1, 1, 0, 0, 2, 1, 0))


if __name__ == "__main__":
    main()
