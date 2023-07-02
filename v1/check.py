import itertools

import numpy as np

from operators import Operator, data

nand_like_ops = {key: item for key, item in data.items() if item.count == 19683}


symmetry_ops = list(get_symmetry_operator())
symmetry_nand_ops = [item for item in symmetry_ops if item.count == 19683]
print(filter_similar_operator(symmetry_nand_ops))
