import itertools

import numpy as np
from alive_progress import alive_bar
from PIL import Image

from model import Operator, session


def check_interchangeability(operators: list[Operator]) -> str:
    """
    It is assumed that all three-valued logic operators are commutative.
    That is, True, False and Unknown can be interchanged without affecting
    the number of states that can be generated.

    Args:
        operators (list[Operator]): All operator objects

    Returns:
        str: Conclusion
    """
    print("checking interchangeability...")
    order = [0, 1, 2]
    with alive_bar(19683 * 6) as bar:
        for op in operators:
            arr = op.to_array()
            for new_order in itertools.permutations(order):
                new_arr = arr.copy()
                for i in range(3):
                    for j in range(3):
                        new_arr[i, j] = new_order[order.index(arr[i, j])]
                new_arr[new_order, :] = new_arr[order, :]
                new_arr[:, new_order] = new_arr[:, order]
                new_op = Operator.query_by_array(new_arr)
                if new_op is None:
                    print(op, new_order, new_arr)
                elif new_op.count != op.count:
                    print(f"{op=}, {new_op=}")
                    return "Guess errors"
                bar()
    return "Guess correct"


# Guess correct


def check_NAND_like(operators: list[Operator]) -> str:
    """
    NAND operator based on Boolean logic.
    First set any two of True, False and Unknown as NAND operators,
    Then explore under what conditions the remaining value can make the operator universal.

    Args:
        operators (list[Operator]): All operator objects

    Returns:
        bool: Conclusion
    """
    ...


def check_symmetry(operators: list[Operator]) -> str:
    """
    Explore the quantitative relationship between operators that conform to diagonal symmetry and universal operators.

    Args:
        operators (list[Operator]): All operator objects

    Returns:
        bool: Conclusion
    """
    print("finding symmetry universal operator...")
    domin = [0, 1, 2]
    count = 0
    for item in itertools.product(*[domin for _ in range(6)]):
        op = Operator.query_by_array(
            np.array(
                [
                    [item[0], item[1], item[3]],
                    [item[1], item[2], item[4]],
                    [item[3], item[4], item[5]],
                ]
            )
        )
        if op.count == 19683:
            count += 1
    return f"{count=}"


# symmetry
# [0 1 3]
# [1 2 4]
# [3 4 5]
# Result = 90


def analyse_value_distribution(operators: list[Operator]) -> str:
    """
    Explore the distribution of True, False and Unknown in all universal operators.

    Args:
        operators (list[Operator]): All operator objects

    Returns:
        str: Conclusion
    """
    print("Analysing value distribution...")
    init = [0, 0, 0]
    count = [[init.copy() for _ in range(3)] for _ in range(3)]
    for op in operators:
        arr = op.to_array()
        if op.count == 19683:
            for i in range(9):
                count[i // 3][i % 3][arr[i // 3, i % 3]] += 1
    (total_0_count, total_1_count, total_2_count) = (0, 0, 0)
    for line in count:
        for item in line:
            total_0_count += item[0]
            total_1_count += item[1]
            total_2_count += item[2]

    # Show by image
    img = Image.new(mode="RGB", size=(300, 300))
    for i in range(3):
        for j in range(3):
            color = tuple([int(item / 1887 * 256) for item in count[i][j]])
            new_img = Image.new(mode="RGB", size=(100, 100), color=color)
            img.paste(new_img, (i * 100, j * 100))
    img.save("value_distribution.jpg")
    return "\n".join(str(item) for item in count) + f"\n{total_0_count=}, {total_1_count=}, {total_2_count=}"


# Result
# [0, 1887, 1887], [1167, 1167, 1440], [1167, 1440, 1167]
# [1167, 1167, 1440], [1887, 0, 1887], [1440, 1167, 1167]
# [1167, 1440, 1167], [1440, 1167, 1167], [1887, 1887, 0]
# Explanation
# [tt, tf, tm]
# [mt, mm, mf]
# [ft, fm, ff]
# for each, eg. tt = [count 0, count 1, count 2]


if __name__ == "__main__":
    operators = session.query(Operator).all()

    # print("interchangeability", check_interchangeability(operators))

    # print("NAND_like", check_NAND_like(operators))

    print("symmetry", check_symmetry(operators))

    print(analyse_value_distribution(operators))


# Phased conclusions, for all universal operators. If they are overlapped, the value distribution is symmetrical, but for the respective operators, there are not many (90/3774) symmetrical
