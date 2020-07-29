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