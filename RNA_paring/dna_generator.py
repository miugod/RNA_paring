import numpy as np


def generate_single_chain(n, s, random_engine=None):
    """Generate a single DNA chain with length n & max node connect distance s.

    :return if_connect: List<set> with length n.
    """
    if random_engine is None:
        conn = np.random.randint(0, 2, (n, 2 * s)).tolist()
    else:
        conn = random_engine.randint(0, 2, (n, 2 * s)).tolist()
    for i in range(n):
        conn[i] = set(
            [i + j + 1 for j in range(0, s) if conn[i][j] and i + j + 1 < n]
            + [i + j for j in range(-s, 0) if conn[i][j] and i + j >= 0]
        )
    for i in range(n):
        for j in conn[i].copy():
            if i not in conn[j]:
                conn[i].remove(j)  # 删除不能互连的
    for i in range(n):
        for j in conn[i].copy():
            if i + 1 < n and j - 1 in conn[i + 1] and i + 1 != j:
                pass
            elif i - 1 >= 0 and j + 1 in conn[i - 1] and i - 1 != j:
                pass
            else:
                conn[i].remove(j)
                conn[j].remove(i)  # 删除不能成对 pair 出现的

    conn = [sorted(list(x)) for x in conn]
    return conn


if __name__ == "__main__":
    roll = generate_single_chain(24, 8)
    print(roll)
