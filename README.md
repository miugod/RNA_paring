# RNA配对验证算法
方法1：使用“从零开始的间隔为s的动态规划”，与穷举法（一定正确）比较，出现了不可避免的少数错误。
方法2：回溯至m-2s法，与穷举法比较，出现不可避免的少数错误。
方法3：从零开始到n结束的、间隔为2s的动态规划算法，除连续结构有时无法取得最优解，RNA很少有这种结构所以截至目前没有生成错例。一个启发式算法

