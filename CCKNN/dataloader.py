from ICCStandard.ICCStandard import IDataLoader

class DataLoader(IDataLoader):
    def __init__(self, file_name, ignore_first_row=False):
        self.read_data_set(file_name, ignore_first_row)
        self.verify_data()
        self.process_data()

    '''
    读取数据
    '''
    def read_data_set(self, file_name, ignore_first_row=False):
        with open(file_name, encoding='utf-8') as f:
            ori_list = f.read().split('\n')
        if ignore_first_row:
            ori_list = ori_list[1:]
        self.train_list = []
        for line in ori_list:
            line = line.strip().split(',')
            for i in range(len(line) - 1):
                line[i] = float(line[i])
            self.train_list.append(line)
    
    '''
    验证数据
    '''
    def verify_data(self):
        if len(self.train_list) == 0:
            raise Exception("Train data is empty.")
        col_num = len(self.train_list[0])
        if col_num < 2:
            raise Exception("The size is less than 2 (the data set must with at least 1 attribute and 1 label) at line 0.")
        for idx, item in enumerate(self.train_list):
            if len(item) != col_num:
                raise Exception("The size at line {} is not match with the first row, which should be {} but {}.".format(idx, col_num, len(item)))

    '''
    处理数据
    '''
    def process_data(self):
        self.X_train = []
        self.Y_train = []
        for item in self.train_list:
            self.X_train.append(item[:len(item) - 1])
            self.Y_train.append(item[len(item) - 1])