from planar_RNA_generator import rna_planar
from dna_generator import generate_single_chain
from multiprocessing import Lock, Pool
import numpy as np
from solvers import Solver2sThreading as Solver
from solvers.exhaustive import exhaustive
import timeit
from threading import Lock
from unit_test import get_units
from utils.average_meter import AverageMeter
from utils.logger import setup_logger


log_lock = Lock()  # 输出锁


def main():
    logger = setup_logger("RNA_Connect_Alg", "log", 0)
    logger.info("Validation begin.")
    logger.info("-" * 10)

    val_epoch(55, 10, 50, logger, False)


def val_epoch(n, s, rounds, logger, only_test_time=False):
    """根据给定 n, s 验证 rounds 次结果正确性."""
    logger.info("Validation: n={}, s={}, rounds={}".format(n, s, rounds))
    pool = Pool(processes=8)  # 最多同时算50个
    processes = []

    if only_test_time:
        dp_timer = AverageMeter()
        for i in range(rounds):
            # cost = val_once(n, s, logger, "{}/{}".format(i + 1, rounds), only_test_time)
            # dp_timer.update(cost)
            processes.append(
                pool.apply_async(
                    val_once,
                    (
                        n,
                        s,
                        logger,
                        "{}/{}".format(i + 1, rounds),
                        only_test_time,
                        np.random.RandomState(),
                    ),
                )
            )
        for p in processes:
            cost = p.get()
            dp_timer.update(cost)
        pool.close()
        pool.join()

        logger.info(
            "DP法 平均损耗时间 {}ms, 最小/最大损耗时间 {}/{}ms.".format(
                dp_timer.avg, dp_timer.min, dp_timer.max
            )
        )
        logger.info("End validation epoch.")
        logger.info("-" * 10)
    else:
        correct = 0
        exh_timer, dpnew_timer = AverageMeter(), AverageMeter()
        for i in range(rounds):
            # cost1, cost3, if_correct = val_once(
            # n, s, logger, "{}/{}".format(i + 1, rounds)
            # )
            # exh_timer.update(cost1)
            # dpnew_timer.update(cost3)
            # correct += 1 if if_correct else 0
            processes.append(
                pool.apply_async(
                    val_once,
                    (
                        n,
                        s,
                        logger,
                        "{}/{}".format(i + 1, rounds),
                        False,
                        np.random.RandomState(),
                    ),
                )
            )
        for p in processes:
            cost1, cost3, if_correct = p.get()
            exh_timer.update(cost1)
            dpnew_timer.update(cost3)
            correct += 1 if if_correct else 0
        pool.close()
        pool.join()

        logger.info("DP 结果验证 正确数/全部数: {}/{}".format(correct, rounds))
        logger.info(
            "穷举法 平均损耗时间 {}ms, 最小/最大损耗时间 {}/{}ms.".format(
                exh_timer.avg, exh_timer.min, exh_timer.max
            )
        )
        # logger.info('DP法 平均损耗时间 {}ms, 最小/最大损耗时间 {}/{}ms.'.format(dp_timer.avg, dp_timer.min, dp_timer.max))
        logger.info(
            "DPnew法 平均损耗时间 {}ms, 最小/最大损耗时间 {}/{}ms.".format(
                dpnew_timer.avg, dpnew_timer.min, dpnew_timer.max
            )
        )
        logger.info("End validation epoch.")
        logger.info("-" * 10)


def val_once(n, s, logger, count_str="", only_test_time=False, random_engine=None):
    """根据给定 n, s 验证一次 穷举法 vs DP法."""
    #conn = rna_planar(n, s, random_engine)
    conn = rna_planar(n, s, random_engine)
    # exhaustive
    if not only_test_time:
        begin = timeit.default_timer()
        ans_1, ans_seq_1 = exhaustive(conn)
        end = timeit.default_timer()
        time_cost_1 = int((end - begin) * 1000)

    # dp
    # begin2 = timeit.default_timer()
    # ans_2, ans_seq_2 = dp_solver(conn, s)
    # end2 = timeit.default_timer()
    # time_cost_2 = int((end2 - begin2) * 1000)

    # dpnew
        begin3 = timeit.default_timer()
        ans_3, ans_seq_3 = Solver(conn, s).solve()
        end3 = timeit.default_timer()
        time_cost_3 = int((end3 - begin3) * 1000)

    with log_lock:
        if not only_test_time:
            if ans_1 != ans_3:
                correct = False
                logger.warning("-" * 10)
                logger.warning("[{}] 验证结果错误！".format(count_str))
                logger.warning("exh结果为 {}, dpnew结果为 {}.".format(ans_1, ans_3))
                logger.warning("exh连接序列为 {}, dpnew结果为 {}.".format(ans_seq_1, ans_seq_3))
                logger.warning("conn_permit 为 {}".format(conn))
                logger.warning("-" * 10)
            else:
                correct = True
                logger.info(
                    "[{}] 正确. Result={}. Time={}/{}ms.".format(
                        count_str, ans_1, time_cost_1, time_cost_3
                    )
                    
                )
                logger.debug("Time={}/{}ms".format(time_cost_1, time_cost_3))
                print("conn_permit 为 {}".format(conn))
        else:
            logger.debug("[{}] Time={}ms.".format(count_str, time_cost_3))

    if only_test_time:
        return time_cost_3
    return time_cost_1, time_cost_3, correct


# def unit_test():
#     units = get_units()
#     for conn, ans in units:
#         res = dp_solver(conn, 10)
#         print(res[0] == ans, res)


if __name__ == "__main__":
    main()
