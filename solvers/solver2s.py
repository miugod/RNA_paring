import numpy as np

try:
    from exhaustive import exhaustive, check_if_legal
except ImportError:
    from .exhaustive import exhaustive, check_if_legal


class Solver2s:
    def __init__(self, conn, s):
        self.dp = {}
        self.conn = conn
        self.s = s

    def solve(self):
        self.f(0, len(self.conn))
        return self.f(0, len(self.conn))

    def f(self, i, j):
        """动态规划[i, j]范围。使用多线程。

        Args:
            i (int): left.
            j (int): right.

        Returns:
            int: score.
            list: sequence.
        """
        if (i, j) in self.dp.keys():
            return self.dp[(i, j)]
        self.dp[(i, j)] = (0, np.array([-1 for _ in range(j - i)]).astype(np.int32))
        if j - i <= 3:  # 长度<4则解为0
            return self.dp[(i, j)]
        elif j - i < 4 * self.s + 1:  # 直接遍历
            ans, seq = exhaustive(self.conn[:j], start_index=i)
            self.dp[(i, j)] = (ans, seq[i:j])
            return self.dp[(i, j)]

        # do dp
        interval = 2 * self.s  # 中间间隔多少用于穷举
        for k in range(i + 1, j - interval - 1):
            self.solve_interregional(i, j, k, interval)
        return self.dp[(i, j)]

    def solve_interregional(self, i, j, k, interval):
        # 在这里使用多线程，因为不同iter变量互不影响，且可并行。唯需注意self.dp复制时的线程不安全现象。
        left, right = self.f(i, k), self.f(k + interval, j)
        concat = np.concatenate(
            (
                [-1 for _ in range(i)],
                left[1],
                [-1 for _ in range(interval)],
                right[1],
            ),
            axis=0,
        ).astype(np.int32)
        limit_left, limit_right = max(i, k - self.s), min(j, k + interval + self.s)
        solution = (left[0] + right[0], concat)
        solution = self.dfs(concat, i, solution[0], solution, limit_left, limit_right)
        if self.dp[(i, j)][0] < solution[0]:
            self.dp[(i, j)] = (solution[0], solution[1][i:j])

    def dfs(self, status, begin, score, solution, limit_left, limit_right):
        """中间段落的遍历。由于solution不断变化，无法使用多线程。"""
        if begin == limit_right:
            if score > solution[0] and check_if_legal(status):
                solution = (score, status)
            return solution
        if status[begin] > -1:
            return self.dfs(status, begin + 1, score, solution, limit_left, limit_right)
        for connect in self.conn[begin]:
            if connect < limit_left or connect >= limit_right:  # 超出2s范围不穷举
                continue
            if status[connect] > -1 or connect < begin:  # 全穷举不回测
                continue
            tmp = status.copy()
            tmp[begin], tmp[connect] = connect, begin
            solution = self.dfs(
                tmp, begin + 1, score + 2, solution, limit_left, limit_right
            )
            del tmp
        return self.dfs(status, begin + 1, score, solution, limit_left, limit_right)


if __name__ == "__main__":
    # conn = [[], [8], [7], [8, 10], [7, 9, 10], [6, 9], [5], [2, 4, 10, 14], [1, 3, 9, 13], [4, 5, 8], [3, 4, 7], [], [], [8], [7], [20, 22], [19, 21], [24], [21, 23], [16, 20], [15, 19], [16, 18, 24], [15, 23], [18, 22], [17, 21], [], [29], [28], [27], [26]]
    # conn = [
    #     [4, 6],
    #     [3, 5],
    #     [],
    #     [1, 8],
    #     [0, 7],
    #     [1, 6],
    #     [0, 5],
    #     [4],
    #     [3],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [18, 21],
    #     [17, 20],
    #     [16, 22],
    #     [15, 21],
    #     [],
    #     [16, 24],
    #     [15, 18, 23],
    #     [17],
    #     [21],
    #     [20],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    #     [],
    # ]

    conn = [
        [],
        [6],
        [5],
        [7],
        [6],
        [2, 11],
        [1, 4, 10],
        [3, 9],
        [],
        [7],
        [6],
        [5],
        [],
        [17],
        [16],
        [18],
        [14, 17, 22],
        [13, 16, 21],
        [15],
        [25],
        [24],
        [17, 23, 27],
        [16, 26],
        [21],
        [20, 27],
        [19, 26],
        [22, 25],
        [21, 24],
        [],
        [],
    ]  # supposed to be 8 but not 4
    # []
    s = 7
    solver = Solver2s(conn, s)
    res = solver.solve()
    print(res)
    # print(" ".join([str(x) for x in (res[1])]))
