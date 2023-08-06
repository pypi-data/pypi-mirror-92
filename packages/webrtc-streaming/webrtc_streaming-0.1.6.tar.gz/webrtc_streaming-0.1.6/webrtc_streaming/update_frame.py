import grpc
from webrtc_streaming.autogen import (
    webrtc_streaming_pb2 as webrtc_streaming_pb2
)
from webrtc_streaming.autogen import (
    webrtc_streaming_pb2_grpc as webrtc_streaming_pb2_grpc
)


def update_frame(ip_server=None,
                 data=None,
                 width=None,
                 height=None):
    try:
        assert ip_server is not None
        assert data is not None
        assert isinstance(width, int)
        assert isinstance(height, int)
        frame = webrtc_streaming_pb2.Frame(
            data=data, width=width, height=height)
        channel = grpc.insecure_channel(ip_server)
        stub = webrtc_streaming_pb2_grpc.WebRTC_StreamingStub(channel)
        response = stub.UpdateFrame(frame)
        return isinstance(response, webrtc_streaming_pb2.Empty)
    except Exception:
        return False
