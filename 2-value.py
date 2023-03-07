from collections import deque

from typing_extensions import Self


class State:
    def __init__(self, p1: bool, p2: bool, p3: bool, p4: bool) -> None:
        self.state = [
            [p1, p2],
            [p3, p4],
        ]

    def __str__(self) -> str:
        return "\n".join([f"{v}" for v in self.state])

    def _export(self) -> tuple:
        return tuple(self.state[0] + self.state[1])

    @classmethod
    def _import(cls, t: tuple) -> Self:
        return cls(*t)


class Operator:
    def __init__(self, tt: bool, tf: bool, ft: bool, ff: bool) -> None:
        self.cal_map = {
            (True, True): tt,
            (True, False): tf,
            (False, True): ft,
            (False, False): ff,
        }

    def cal(self, formar: State, latter: State) -> State:
        res = []
        for i in range(4):
            res.append(
                self.cal_map[
                    (formar.state[i // 2][i % 2], latter.state[i // 2][i % 2])
                ]
            )
        return State(*res)

    def __str__(self) -> str:
        return f"{self.cal_map}"


def full_arrangement():
    domin = [True, False]
    for p1 in domin:
        for p2 in domin:
            for p3 in domin:
                for p4 in domin:
                    yield (p1, p2, p3, p4)


def check(op: Operator, s1: State, s2: State):
    d = {s1._export()}
    new_que = deque([s2])
    while new_que:
        s = new_que.popleft()
        new: set[State] = set()
        res = op.cal(s, s)
        if res._export() not in d:
            new.add(res._export())
        for t in d:
            old_s = State._import(t)
            res = op.cal(s, old_s)
            if res._export() not in d:
                new.add(res._export())
            res = op.cal(old_s, s)
            if res._export() not in d:
                new.add(res._export())
        for item in new:
            d.add(item)
            new_que.append(State._import(item))

    return d


def main():
    for v in full_arrangement():
        op = Operator(*v)
        s1 = State(True, True, False, False)
        s2 = State(True, False, True, False)
        d = check(op, s1, s2)
        if len(d) == 16:
            print(op)


if __name__ == "__main__":
    main()
