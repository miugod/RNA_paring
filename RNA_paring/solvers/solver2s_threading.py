from concurrent.futures import ThreadPoolExecutor
import numpy as np
import threading

try:
    from exhaustive import exhaustive, check_if_legal
    from solver2s import Solver2s
except ImportError:
    from .exhaustive import exhaustive, check_if_legal
    from .solver2s import Solver2s


class Solver2sThreading(Solver2s):
    def __init__(self, conn, s):
        super().__init__(conn, s)
        self.mutex = threading.Lock()  # self.dp值改变锁
        self.pool = ThreadPoolExecutor(200)  # 最多200个线程的池

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
        threads = []  # 存所有线程返回值，但其实不返回，只是充当阻塞
        for k in range(i + 1, j - interval - 1):
            thread = self.pool.submit(self.solve_interregional, i, j, k, interval)
            threads.append(thread)
        for thread in threads:
            thread.result()  # 阻塞直到计算完成
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
            with self.mutex:  # with外自动解锁
                self.dp[(i, j)] = (solution[0], solution[1][i:j])


if __name__ == "__main__":

    conn = [[7], [6], [], [], [12], [11], [], [], [], [16], [15], [], [17], [16], [], [], [24], [23, 30], [29], [], [], [], [], [], [], [31], [30], [], [], [], [], [], [37], [36], [], [41], [40], [], [43], [42], 
[], [], [51], [50], [], [], [58], [57], [], [], [], [], [], [], [], [], [], [], [], []]
    # []
    s = 13
    solver = Solver2sThreading(conn, s)
    res = solver.solve()
    print(res)
    # print(" ".join([str(x) for x in (res[1])]))
