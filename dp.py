import numpy as np
from exhaustive import exhaustive, check_if_legal


def dp_solver(conn, s):
    """f(0, m) = f(0, k) + o(k-s, m)"""
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
        for i in range(m - 1, max(m - s*2 - 2, -1), -1):  # 前推至 2s
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
    """f(i, j) = f(i, k) + f(k, j) + o(k-s, k+s)"""
    dp = {}

    def f(i, j):
        """求解 [i,j) 区域的最优解.

        Returns:
            ans: 最优值.
            ans_seq: 最优解序列, len == j-i.
        """
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
                """使用 dfs 方式进行穷举.
                
                Args:
                    status: np.ndarray, 当前配对 seq.
                    begin: 深搜开始位.
                    score: 到此为止的最优值.
                """
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


def dp_interval_s_solver(conn, s):
    """f(i, j) = f(i, k) + f(k+s, j) + exh(k-s, k+2s)
    
    Args:
        conn: list, conn_permit, 连接允许数组.
        s: int.
    """
    dp = {}

    def f(i, j):
        """求解 [i,j) 区域的最优解.

        Returns:
            ans: 最优值.
            ans_seq: 最优解序列, len == j-i.
        """
        if (i, j) in dp.keys():
            return dp[(i, j)]
        dp[(i, j)] = (0, np.array([-1 for _ in range(j-i)]).astype(np.int32))
        if j - i <= 3:
            return dp[(i, j)]
        elif j - i <= s:  # 若间距 <= s, 穷举
            conn_ = [list(filter(lambda x: i<=x<j, conn[k])) if k >= i else [] for k in range(j)]  # 仅取[i,j)的conn
            ans, ans_seq = exhaustive(
                conn_,
                start_seq=np.array([-1 for _ in range(j)]),
                start_index=i,
                back_connect=True
            )
            dp[(i, j)] = (ans, ans_seq[i:j])
            return dp[(i, j)]

        # do dp
        for k in range(i+1, j-s):
            left, right = f(i, k), f(k+s, j)
            concat = np.concatenate((
                [-1 for _ in range(i)], 
                left[1], 
                [-1 for _ in range(s)], 
                right[1]), axis=0).astype(np.int32)
            limit_left, limit_right = max(i, k-s), min(j, k+s+s)  # 定义穷举左右界限, 准备穷举
            # solution = (left[0] + right[0], concat)

            # exh(limit_left, limit_right)
            '''
            def dfs(begin, status, score):
                """使用 dfs 方式进行穷举, 可回看.
                
                Args:
                    status: np.ndarray, 当前配对 seq.
                    begin: 深搜开始位.
                    score: 到此为止的最优值.
                """
                # if dfs to the deepest
                if begin == limit_right:
                    nonlocal solution
                    if score > solution[0] and check_if_legal(status):
                        solution = (score, status)
                    return

                # if already connected
                if status[begin] > -1:
                    dfs(begin+1, status, score)
                    return

                # exhaustive
                for connect in conn[begin]:
                    if connect < limit_left or connect >= limit_right:  # 超出2s范围不穷举
                        continue
                    if status[connect] > -1 or connect < begin:  # 全穷举不回测
                        continue
                    tmp = status.copy()
                    tmp[begin], tmp[connect] = connect, begin
                    dfs(begin+1, tmp, score+2)
                    del tmp
                dfs(begin+1, status, score)

            # dfs(i, concat, solution[0])
            '''
            solution = exhaustive(
                conn[:j], 
                start_seq=concat[:j], 
                start_index=limit_left,
                end_index=limit_right,
                back_connect=False)
            if dp[(i, j)][0] < solution[0]:
                dp[(i, j)] = (solution[0], solution[1][i:j])
        return dp[(i, j)]
    f(0, len(conn))
    return f(0, len(conn))


if __name__ == '__main__':
    conn = [[5, 6], [4, 5], [4, 6], [5, 6], [1, 2, 5], [0, 1, 3, 4, 12], [0, 2, 3, 11], [10], [9], [8], [7, 16], [6, 15], [5], [], [], [11, 22], [10, 21], [], [], [], [27], [16, 26], [15], [], [], [], [21], [20], [], []]
    s = 7
    res = dp_new_solver(conn, s)
    print(res)
    res = dp_interval_s_solver(conn, s)
    print(res)
