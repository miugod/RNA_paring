import numpy as np


def exhaustive(conn_permit, start_seq=None, start_index=0, end_index=None, back_connect=True):
    """穷举法解 DNA 配对问题,.

    Args:
        conn_permit: list, 连接允许数组.
        start_seq: np.ndarray, 若半路穷举, 则在此 seq 基础上进行. 必须和 conn 等长.
        start_index: int, if exh from half, start from this index
        end_index: int, 停止穷举位置.
        back_connect: bool, 是否回连. 非半路穷举此值无效.
    Returns:
        ans: int, 最大连接数的值.
        ans_seq: np.ndarray, 达到最大连接的序列.
    """
    n = len(conn_permit)
    end_index = end_index or n
    if start_seq is None:
        back_connect = False  # 不回连
        start_seq = np.array([-1 for _ in range(n)])
    ans = sum(start_seq > -1)  # note max answer
    ans_seq = start_seq  # note which connects which

    def dfs(begin, seq, cur_ans):
        """穷举递归, 不回看.
        
        Args:
            begin: int, 递归开始位.
            seq: np.ndarray, 至此为止的配对序列.
            cur_ans: int, 当前的配对点数. 等于 sum(seq > -1).
        """
        nonlocal ans, ans_seq

        # if dfs to the deepest
        if begin == end_index:
            # ans_cur = sum(seq > -1)  # 旧法
            ans_cur = cur_ans
            if ans_cur > ans and check_if_legal(seq):
                ans, ans_seq = ans_cur, seq
            return

        # if already connected
        if seq[begin] > -1:
            dfs(begin + 1, seq, cur_ans)
            return
        
        # 剪枝: 若递归至此绝无可能超过最优解则剪枝''
        prob_max_conn_num = 0  # 之后可能的最多连接数
        for i in range(begin, end_index):
            if seq[i] == -1 and conn_permit[i] and conn_permit[i][-1] >= begin:
                for j in list(filter(lambda x: begin<=x<end_index, conn_permit[i])):
                    if seq[j] == -1:
                        prob_max_conn_num += 1
                        break
        if cur_ans + prob_max_conn_num <= ans:
            return

        # exhaustive
        for i in conn_permit[begin]:
            if i >= end_index or seq[i] > -1:  # 穷举不能超过止位, 有连接不连
                continue
            if i <= begin and not back_connect:
                continue
            tmp = seq.copy()
            tmp[begin], tmp[i] = i, begin
            dfs(begin + 1, tmp, cur_ans + 2)
            del tmp
        dfs(begin + 1, seq.copy(), cur_ans)  # 这行在 for 前会导致求得的解的熵很高, 即先连后面再连前面

    dfs(start_index, start_seq, sum(start_seq > -1))
    return ans, ans_seq


def check_if_legal(seq):
    """检查一个 seq 是否合法"""
    n = len(seq)
    legal = [seq[i] == -1 for i in range(n)]
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
