# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import basic_pb2 as basic__pb2


class FileStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.upload = channel.stream_unary(
                '/File/upload',
                request_serializer=basic__pb2.FileBody.SerializeToString,
                response_deserializer=basic__pb2.Response.FromString,
                )


class FileServicer(object):
    """Missing associated documentation comment in .proto file."""

    def upload(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'upload': grpc.stream_unary_rpc_method_handler(
                    servicer.upload,
                    request_deserializer=basic__pb2.FileBody.FromString,
                    response_serializer=basic__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'File', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class File(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def upload(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/File/upload',
            basic__pb2.FileBody.SerializeToString,
            basic__pb2.Response.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)


class PredictStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.pred = channel.unary_unary(
                '/Predict/pred',
                request_serializer=basic__pb2.PredictInfo.SerializeToString,
                response_deserializer=basic__pb2.Response.FromString,
                )


class PredictServicer(object):
    """Missing associated documentation comment in .proto file."""

    def pred(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PredictServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'pred': grpc.unary_unary_rpc_method_handler(
                    servicer.pred,
                    request_deserializer=basic__pb2.PredictInfo.FromString,
                    response_serializer=basic__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Predict', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Predict(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def pred(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Predict/pred',
            basic__pb2.PredictInfo.SerializeToString,
            basic__pb2.Response.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
