import numpy as np
from solvers.exhaustive import exhaustive, check_if_legal


def dp_solver(conn, s):
    dp = {}

    def f(m):
        """前 m 项之解"""
        nonlocal dp, conn, s
        if m in dp.keys():
            return dp[m]
        elif m <= 3:  # no result
            dp[m] = (0, np.array([-1 for _ in range(m)]).astype(np.int32))
            return dp[m]

        # do dp
        # for i in range(max(m - s - 1, 0), m):  # 往前看的位数
        # for i in range(m - 1, max(m - s - 2, -1), -1):
        for i in range(m - 1, max(m - s - 2, -1), -1):  # 前推至 2s
            ans, ans_seq = exhaustive(
                conn[:m],
                start_seq=np.append(f(i)[1], [-1 for _ in range(m - i)]),
                start_index=i,
            )
            if m not in dp.keys():
                dp[m] = (ans, ans_seq)
            else:
                if ans > dp[m][0]:
                    dp[m] = (ans, ans_seq)
        return dp[m]

    f(len(conn))
    return f(len(conn))


def dp_new_solver(conn, s):
    dp = {}  # dp.value shape: (ans, sequence[i:j])

    def f(i, j):
        if (i, j) in dp.keys():
            return dp[(i, j)]
        dp[(i, j)] = (0, np.array([-1 for _ in range(j - i)]).astype(np.int32))
        if j - i <= 3:  # 长度<4则解为0
            return dp[(i, j)]
        elif j - i < 4 * s + 1:  # 直接遍历
            ans, seq = exhaustive(conn[:j], start_index=i)
            dp[(i, j)] = (ans, seq[i:j])
            return dp[(i, j)]

        # do dp
        interval = 2 * s  # 中间间隔多少用于穷举
        for k in range(i + 1, j - interval - 1):
            left, right = f(i, k), f(k + interval, j)

            concat = np.concatenate(
                (
                    [-1 for _ in range(i)],
                    left[1],
                    [-1 for _ in range(interval)],
                    right[1],
                ),
                axis=0,
            ).astype(np.int32)
            limit_left, limit_right = max(i, k - s), min(j, k + interval + s)

            solution = (left[0] + right[0], concat)

            def dfs(status, begin, score):
                if begin == limit_right:
                    nonlocal solution
                    if score > solution[0] and check_if_legal(status):
                        solution = (score, status)
                    return
                if status[begin] > -1:
                    dfs(status, begin + 1, score)
                    return
                for connect in conn[begin]:
                    if connect < limit_left or connect >= limit_right:  # 超出2s范围不穷举
                        continue
                    if status[connect] > -1 or connect < begin:  # 全穷举不回测
                        continue
                    tmp = status.copy()
                    tmp[begin], tmp[connect] = connect, begin
                    dfs(tmp, begin + 1, score + 2)
                    del tmp
                dfs(status, begin + 1, score)

            dfs(concat, i, solution[0])
            if dp[(i, j)][0] < solution[0]:
                dp[(i, j)] = (solution[0], solution[1][i:j])
        return dp[(i, j)]

    f(0, len(conn))
    return f(0, len(conn))


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
    res = dp_new_solver(conn, s)
    print(res)
    # print(" ".join([str(x) for x in (res[1])]))
