import numpy as np


def exhaustive(conn_permit, start_seq=None, start_index=0):
    """
    :param conn_permit:
    :param start_seq:(np.ndarray) if exh from half, use this seq
    :param start_index: if exh from half, start from this index
    """
    n = len(conn_permit)
    if start_seq is None:
        from_half = False  # exhaustive from half
        start_seq = np.array([-1 for _ in range(n)])
    else:
        from_half = True
    ans = sum(start_seq > -1)  # note max answer
    ans_seq = start_seq  # note which connects which

    def dfs(begin, seq):
        if begin == n:  # if dfs to the deepest
            nonlocal ans, ans_seq
            ans_cur = sum(seq > -1)
            if ans_cur > ans and check_if_legal(seq):
                ans, ans_seq = ans_cur, seq
            return

        if seq[begin] > -1:  # if already connected
            dfs(begin + 1, seq)
            return

        # exhaustive
        for i in conn_permit[begin]:
            if i >= n or seq[i] > -1 or i <= begin and not from_half:  # 全穷举不回测
                continue
            tmp = seq.copy()
            tmp[begin], tmp[i] = i, begin
            dfs(begin + 1, tmp)
            del tmp
        dfs(begin + 1, seq.copy())  # 这行在 for 前会导致求得的解的熵很高, 及先连后面再连前面

    dfs(start_index, start_seq)  # dfs(0, np.array([-1 for _ in range(n)])) if not from_half
    return ans, ans_seq


def check_if_legal(seq):
    n = len(seq)
    legal = [True if seq[i] == -1 else False for i in range(n)]
    for i in range(n):
        if legal[i]:
            continue
        if n - 1 > i != seq[i + 1] and seq[i + 1] == seq[i] - 1:
            legal[i] = legal[i+1] = legal[seq[i]] = legal[seq[i+1]] = True
        elif 0 < i != seq[i - 1] and seq[i - 1] == seq[i] + 1:
            legal[i] = legal[i-1] = legal[seq[i]] = legal[seq[i-1]] = True
        else:
            return False
    return True


if __name__ == '__main__':
    # from dna_generator import generate_single_chain
    # chain = generate_single_chain(40, 10)
    # ans, seq = exhaustive(chain)
    # print(ans, seq, chain)
    conn = [[6], [5, 8], [7], [6], [5],
            [1, 4], [0, 3], [2], [1, 11], [10, 17],
            [9, 15, 16], [8, 14, 18], [16, 17], [15, 16], [11, 15],
            [10, 13, 14, 21], [10, 12, 13, 20], [9, 12], [11], [],
            [16], [15, 24, 25], [23, 24], [22, 29], [21, 22, 28],
            [21], [], [32], [24, 31], [23, 30],
            [29], [28, 34, 39], [27, 33, 38], [32, 39], [31, 37, 38],
            [36, 37], [35], [34, 35], [32, 34], [31, 33]]







    print(exhaustive(conn))
