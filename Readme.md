# CCKNN 集群部署样例代码

[项目Github](https://github.com/aleversn/CCKNN)

目录结构
```html
└─ root
   ├─ CCKNN //算法主体结构, 重写了ICCStandard
   │  ├─ dataloader.py
   |  ├─ model.py
   |  └─ predict.py
   ├─ ICCStandard
   |  └─ ICCStandard.py
   ├─ basic.proto
   ├─ server.py
   ├─ client.py
   ├─ test.py
   ├─ Readme.md
   └─ LICENSE

```

## Dokcer

1. 确保提前安装好`Docker`并执行以下命令创建镜像:

```powershell
docker run --name [name]  -p [host_port]:[docker_port] [image_name]
```

2. 进入镜像开发

## 使用标准化封装接口`ICCStandard`进行代码结构优化

参考:
- [机器学习工程化结构接口](http://molihua.fzu.edu.cn/zh/master/ml/lpc/r6)
{.links-list}

1. 根据项目需求引入相关接口, 如引入数据加载器:

```python
from ICCStandard.ICCStandard import IDataLoader
```

2. 完善接口内容.

3. 尽量确保最后仅需引用`train.py`和`predict.py`两个文件. 例如, 在`CCKNN`中我们重写了`IDataloader`, `IModel`和`IPredict`. 在`predict.py`中, 我们引用了前两者, 使得使用者仅需调用`predict.py`即可.

> 因为`KNN`是懒监督学习, 所以我们不需要定义`ITrainer`. 同时示例代码也没有定义`IAnalysis`.

```python
# predict.py

import numpy as np
from ICCStandard.ICCStandard import IPredict
from CCKNN.dataloader import DataLoader
from CCKNN.model import Model

class Predicter(IPredict):
    def __init__(self, train_file_name, ignore_first_row=False):
        self.model_init()
        self.dataloader = DataLoader(train_file_name, ignore_first_row)
    
    def model_init(self):
        self.model = Model().get_model()

    def data_process(self):
        return 0

    def pred(self, X, k=3):
        return self.model(x_train=np.array(self.dataloader.X_train), x_test=np.array(X), y_train=self.dataloader.Y_train, k=k)
```

4. 测试模型功能

```python
from CCKNN.predict import Predicter

predicter = Predicter('./train.csv', True)
predicter.pred([3,2])
```

## 编写gRPC接口

参考:
- [基于grpc的流式方式实现双向通讯(Python)](http://molihua.fzu.edu.cn/sosd/web/wiki/grpc/stream_python)
{.links-list}

安装

```powershell
pip install grpcio
pip install grpcio-tools
```

1. 定义接口

`basic.proto`

```protobuf
syntax = "proto3";

service File {
    rpc upload (stream FileBody) returns (Response);
}

service Predict {
    rpc pred (PredictInfo) returns (Response);
}

message PredictInfo {
    string guid = 1;
    repeated float X = 2;
    int32 k = 3;
    bool ignore_first_row = 4;
}

message Response {
    string status = 1;
    string result = 2;
}

message FileBody {
    bytes file = 1;
}
```

- 接口包含2个服务: `File`和`Predict`, 我们定义了上传数据集的服务和预测的服务.
- 信息载体包含3种: 
    - `PredictInfo`: 携带训练集文件的`GUID`, 要预测的数组`X`, 近邻`k`的大小, 以及是否忽略首行表头.
    - `Response`: 携带状态和说明, `status`用来表示运行状态, `result`用来表示具体的说明或要返回的结果.
    - `FileBody`: 携带文件字节数据, 用于传输文件.

2. 编译`basic.proto`

```powershell
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. basic.proto
```

得到`basic_pb2.py`和`basic_pb2_grpc.py`两个文件.

3. 编写服务端代码

```python
# server.py

from concurrent import futures
import os
import time
import uuid
import grpc
import basic_pb2
import basic_pb2_grpc
from CCKNN.predict import Predicter

class File(basic_pb2_grpc.FileServicer):

    def upload(self, request, context):
        if not os.path.isdir('./temp'):
            os.makedirs('./temp')
        guid = str(uuid.uuid1()).split('-')[0]
        with open('./temp/{}'.format(guid), 'ab') as f:
            for r in request:
                f.write(r.file)
        return basic_pb2.Response(status='success', result=guid)

class Predict(basic_pb2_grpc.PredictServicer):

    def pred(self, request, context):
        guid = request.guid
        predicter = Predicter('./temp/{}'.format(guid), request.ignore_first_row)
        result = predicter.pred(request.X, request.k)
        return basic_pb2.Response(status="success", result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    basic_pb2_grpc.add_FileServicer_to_server(File(), server)
    basic_pb2_grpc.add_PredictServicer_to_server(Predict(), server)
    server.add_insecure_port('[::]:80')
    server.start()

    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
```

编写客户端测试数据

```python
# client.py

# %%
import grpc
import basic_pb2
import basic_pb2_grpc
from tqdm import tqdm

# %%
def sendfile():
    channel = grpc.insecure_channel('localhost:80')

    stub = basic_pb2_grpc.FileStub(channel)
    def readfile():
        with open('train.csv', 'rb') as f:
            lines = f.readlines()
            for line in tqdm(lines):
                yield basic_pb2.FileBody(file=line)
    response = stub.upload(readfile())
    print('Upload Return: {}'.format(response))

sendfile()
```

```python
# %%
def pred():
    channel = grpc.insecure_channel('localhost:80')

    stub = basic_pb2_grpc.PredictStub(channel)
    response = stub.pred(basic_pb2.PredictInfo(guid="8300884e", X=[3,2], k=3, ignore_first_row=True))
    print(response)

pred()
```