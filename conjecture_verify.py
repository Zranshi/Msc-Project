# conjecture: For each operator, some kind of transformation is performed on it, which can obtain the same number of states.
# That is, suppose there is such an operator p, 0 p 0 = 1, 0 p 2 = 0, and all others are 2. Then there is an operator q, and 0 and 1 in all operation rules of q are swapped. Then we can get The specific operation rules of q: 1 p 1 = 0, 1 p 2 = 1, and all other operations are 2.
# Moreover, the number of states that p and q can obtain from the initial state is the same.
import itertools


class Operator:
    def __init__(self, line: str) -> None:
        pairs = [item.split(":") for item in line[:-1].split(" ")]
        self.line = line
        self.mapping = []
        for pair in pairs:
            key, value = pair
            self.mapping.append((key[0], key[2], value))
        self.mapping.sort(key=lambda x: x)
        self.mapping = tuple(self.mapping)

    def generate_conjecture_operator(self):
        res: list[Operator] = []
        elements = ["0", "1", "2"]

        for mapping in itertools.permutations(elements):
            new_line = []
            for ch in self.line:
                if ch in elements:
                    ch = mapping[elements.index(ch)]
                new_line.append(ch)
            new_line = "".join(new_line)
            res.append(Operator(new_line))
        return res


def main():
    with open("./NAND-like-operator", "r") as read_f:
        lines = read_f.readlines()
    s: set[dict] = set()
    op_list: list[Operator] = []
    for line in lines:
        op = Operator(line)
        op_list.append(op)
        s.add(op.mapping)

    for op in op_list:
        for transfer_op in op.generate_conjecture_operator():
            if transfer_op.mapping not in s:
                print(f"Misconjecture: {op.line}, {transfer_op.line}")


if __name__ == "__main__":
    main()

# OUTPUT
# Misconjecture: 0,0:2 0,1:2 0,2:1 1,0:1 1,1:0 1,2:2 2,0:2 2,1:0 2,2:0, 2,2:0 2,1:0 2,0:1 1,2:1 1,1:2 1,0:0 0,2:0 0,1:2 0,0:2
# Misconjecture: 0,0:1 0,1:2 0,2:1 1,0:1 1,1:0 1,2:0 2,0:2 2,1:1 2,2:0, 2,2:0 2,0:1 2,1:0 0,2:0 0,0:2 0,1:2 1,2:1 1,0:0 1,1:2
# Misconjecture: 0,0:2 0,1:1 0,2:0 1,0:2 1,1:2 1,2:1 2,0:1 2,1:0 2,2:1, 1,1:2 1,0:0 1,2:1 0,1:2 0,0:2 0,2:0 2,1:0 2,0:1 2,2:0
# Misconjecture: 0,0:1 0,1:0 0,2:1 1,0:2 1,1:0 1,2:0 2,0:0 2,1:2 2,2:1, 0,0:2 0,2:0 0,1:2 2,0:1 2,2:0 2,1:0 1,0:0 1,2:1 1,1:2
# Misconjecture: 0,0:1 0,1:0 0,2:2 1,0:2 1,1:2 1,2:0 2,0:1 2,1:2 2,2:1, 1,1:2 1,2:1 1,0:0 2,1:0 2,2:0 2,0:1 0,1:2 0,2:0 0,0:2


# Analysis: For most of the results, it is valid, but there are a small number of failures. I don't know what the reason is. It may be that the conjecture is wrong, or there is an error in the result of NAND-like-operator.
