import numpy as np
import operator
from ICCStandard.ICCStandard import IModel

class Model(IModel):
    def __init__(self):
        self.load_model()
    
    '''
    加载外部模型主体, 完成模型配置
    '''
    def load_model(self):
        self.model = self.knn
    
    '''
    获取最终模型主体
    '''
    def get_model(self):
        return self.model
    
    @staticmethod
    def knn(x_train, x_test, y_train, k):
        train_row = x_train.shape[0]

        # 计算训练样本和测试样本的差值
        diff = np.tile(x_test, (train_row, 1)) - x_train
        # 计算差值的平方和
        sqrDiff = diff ** 2
        sqrDiffSum = sqrDiff.sum(axis=1)
        # 计算距离
        distances = sqrDiffSum ** 0.5
        # 对所得的距离从低到高进行排序
        sortDistance = distances.argsort()
        
        count = {}
        
        for i in range(k):
            vote = y_train[sortDistance[i]]
            count[vote] = count.get(vote, 0) + 1
        # 对类别出现的频数从高到低进行排序
        sortCount = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
        
        # 返回出现频数最高的类别
        return sortCount[0][0]