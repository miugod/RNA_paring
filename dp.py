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
        for i in range(m - 1, max(m - s -2 , -1), -1):  # 前推至 2s
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
    #conn = [[], [8], [7], [8, 10], [7, 9, 10], [6, 9], [5], [2, 4, 10, 14], [1, 3, 9, 13], [4, 5, 8], [3, 4, 7], [], [], [8], [7], [20, 22], [19, 21], [24], [21, 23], [16, 20], [15, 19], [16, 18, 24], [15, 23], [18, 22], [17, 21], [], [29], [28], [27], [26]]
    conn = [[3],[2],[1],[0],[],[8,12],[7,11],[6,14],[5,11,13],[10,14],[9,13],[6,8],[5],[8,10],[7,9],[22],[21],[],[],[22,25,26],[21,24,25],[16,20,26,28],[15,19,25,27],[24],[20,23],[19,20,22],[19,21],[22],[21],[]]
    #conn = [[], [], [5, 9], [4, 8], [3, 9], [2, 8], [12], [11], [3, 5, 10], [2, 4], [8], [7], [6, 18], [16, 17], [15, 16], [14, 20], [13, 14, 19, 20], [13, 19], [12], [16, 17], [15, 16, 27], [26], [28], [27], [], [], [21], [20, 23], [22], []]  #supposed to be 20 but not 18
    #conn = []
    s = 7
    res = dp_new_solver(conn, s)
    print(res)
