from measure import Measure

class DistanceConsistency(Measure):
    def measure(self, proj, label):
        pass


# 实现一段代码，
# 输入：二维数据点，数据点的类别标签
# 输出：一个值
# 过程：
# 1. 首先定义一个函数，叫做质心距离，输入所有的数据点，输出一个bool数组，其中第i个值是代表第i个数据点到他所在聚类的质心的距离小于，其到任意其他聚类的质心的距离。
# 2. 然后，利用质心距离，计算距离一致性。具体
