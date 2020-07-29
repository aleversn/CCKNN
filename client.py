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

# %%
def pred():
    channel = grpc.insecure_channel('localhost:80')

    stub = basic_pb2_grpc.PredictStub(channel)
    response = stub.pred(basic_pb2.PredictInfo(guid="8300884e", X=[3,2], k=3, ignore_first_row=True))
    print(response)

pred()