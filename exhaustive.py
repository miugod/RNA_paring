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

    # conn = [{3, 6}, {4, 5}, {4, 5}, {0, 9}, {1, 2, 7, 8}, {1, 2, 8}, {0, 9}, {4}, {4, 5}, {3, 6}]
    # ans, seq = exhaustive(conn, np.array([-1 for _ in range(10)]), 3)
    # print(ans, seq)

    conn = [[3], [5, 6, 8, 9], [3, 4, 7, 8, 9], [0, 2, 8, 10], [2, 7, 12], [1, 9, 11, 13], [1], [2, 4, 9, 13, 14], [1, 2, 3, 12, 13, 14, 15], [1, 2, 5, 7, 12, 15, 17], [3, 12, 13, 17], [5, 14, 16, 17], [4, 8, 9, 10, 14, 15, 20], [5, 7, 8, 10, 18, 21], [7, 8, 11, 12, 16, 22], [8, 9, 12, 21], [11, 14, 17, 20], [9, 10, 11, 16, 20, 21], [13, 21, 22], [], [12, 16, 17, 22, 23], [13, 15, 17, 18], [14, 18, 20], [20]]
    s = 8
    print(exhaustive(conn[:9]))
