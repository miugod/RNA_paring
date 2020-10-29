import numpy as np
from exhaustive import exhaustive, check_if_legal


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
        for i in range(m - 1, max(m - s*2 -2 , -1), -1):  # 前推至 2s
            ans, ans_seq = exhaustive(conn[:m],
                                      start_seq=np.append(f(i)[1], [-1 for _ in range(m-i)]),
                                      start_index=i)
            if m not in dp.keys():
                dp[m] = (ans, ans_seq)
            else:
                if ans > dp[m][0]:
                    dp[m] = (ans, ans_seq)
        return dp[m]

    f(len(conn))
    return f(len(conn))


def dp_new_solver(conn, s):
    dp = {}

    def f(i, j):
        if (i, j) in dp.keys():
            return dp[(i, j)]
        dp[(i, j)] = (0, np.array([-1 for _ in range(j-i)]).astype(np.int32))
        if j - i <= 3:
            return dp[(i, j)]

        # do dp
        for k in range(i+1, j-1):
            left, right = f(i, k), f(k, j)
            concat = np.concatenate(([-1 for _ in range(i)], left[1], right[1]), axis=0).astype(np.int32)
            limit_left, limit_right = max(i, k-s), min(j, k+s)
            solution = (left[0] + right[0], concat)

            def dfs(status, begin, score):
                if begin == limit_right:
                    nonlocal solution
                    if score > solution[0] and check_if_legal(status):
                        solution = (score, status)
                    return
                if status[begin] > -1:
                    dfs(status, begin+1, score)
                    return
                for connect in conn[begin]:
                    if connect < limit_left or connect >= limit_right:  # 超出2s范围不穷举
                        continue
                    if status[connect] > -1 or connect < begin:  # 全穷举不回测
                        continue
                    tmp = status.copy()
                    tmp[begin], tmp[connect] = connect, begin
                    dfs(tmp, begin+1, score+2)
                    del tmp
                dfs(status, begin+1, score)

            dfs(concat, i, solution[0])
            if dp[(i, j)][0] < solution[0]:
                dp[(i, j)] = (solution[0], solution[1][i:j])
        return dp[(i, j)]
    f(0, len(conn))
    return f(0, len(conn))


if __name__ == '__main__':
    # conn = [[], [5, 8, 9], [4, 7, 8, 9], [8], [2, 7, 12], [1, 11], [], [2, 4, 13, 14], [1, 2, 3, 12, 13], [1, 2, 12], [17], [5, 16], [4, 8, 9, 15], [7, 8], [7, 22], [12, 21], [11, 20], [10], [], [], [16], [15], [14], []]
    conn = [[], [], [], [], [], [], [], [], [16], [15], [14], [13], [20], [11, 19], [10, 17], [9, 16], [8, 15], [14], [], [13], [12], [], [], []]  # result=10
    s = 8
    res = dp_new_solver(conn, s)
    print(res)
