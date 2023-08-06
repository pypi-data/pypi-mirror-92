import asyncio
import logging
import threading
import numpy as np
from enum import Enum
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc import VideoStreamTrack
from aiortc.contrib.media import MediaPlayer
from grpc.experimental import aio
from webrtc_streaming.autogen import (
    webrtc_streaming_pb2_grpc as pb2_grpc
)
from webrtc_streaming.autogen import (
    webrtc_streaming_pb2 as webrtc_streaming_pb2_pb2
)
from webrtc_streaming.remote import start as communicate_with_signaling_server
from av import VideoFrame


class CV2Track(VideoStreamTrack):
    """
    A video stream that returns an cv2 track
    """

    def __init__(self):
        super().__init__()  # don't forget this!
        self.img = np.random.randint(
            255, size=(640, 480, 3), dtype=np.uint8)

    async def recv(self):
        pts, time_base = await self.next_timestamp()

        # create video frame
        frame = VideoFrame.from_ndarray(self.img, format="bgr24")
        frame.pts = pts
        frame.time_base = time_base

        return frame


class VideoSource(Enum):
    H264_RTP = 1
    CV2 = 2


class WebRTC_Streaming_Service(pb2_grpc.WebRTC_StreamingServicer):
    def __init__(self, rtp_video_port, video_source):
        self.pcs = set()
        self.rtp_video_port = rtp_video_port
        self.player = None
        self.cv2_track = None
        self.video_source = video_source

    async def UpdateFrame(self, request, context):
        """
            Update frame only for CV2 video source type
        """
        frame = request
        data = frame.data
        width = frame.width
        height = frame.height
        if self.cv2_track is not None:
            self.cv2_track.img = np.fromstring(
                data, np.uint8).reshape((height, width, 3))
        response = webrtc_streaming_pb2_pb2.Empty()
        return response

    async def Negotiate(self, request, context):
        message = request
        sdp = message.sdp
        type_ = message.type

        assert self.video_source is not None, "video source is not set"

        offer = RTCSessionDescription(sdp=sdp, type=type_)

        pc = RTCPeerConnection()
        self.pcs.add(pc)

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("ICE connection state is %s" % pc.iceConnectionState)
            if pc.iceConnectionState == "failed":
                await pc.close()
                self.pcs.discard(pc)

        # When video source type is RTP_H264
        if self.player is None and self.video_source == VideoSource.H264_RTP:
            f = open("/tmp/webrtc_streaming.sdp", "w+")
            sdp = "c=IN IP4 0.0.0.0\n"
            sdp += "m=video %s RTP/AVP 96\n" % self.rtp_video_port
            sdp += "a=rtpmap:96 H264/90000"

            f.write(sdp)
            f.close()

            options = {"protocol_whitelist": "file,rtp,udp",
                       "buffer_size": "20000000"}
            self.player = MediaPlayer(
                "/tmp/webrtc_streaming.sdp", options=options)

        # When video source type is CV2
        if self.cv2_track is None and self.video_source == VideoSource.CV2:
            self.cv2_track = CV2Track()

        await pc.setRemoteDescription(offer)

        if self.video_source == VideoSource.H264_RTP:
            for t in pc.getTransceivers():
                if t.kind == "audio" and self.player.audio:
                    pc.addTrack(self.player.audio)
                elif t.kind == "video" and self.player.video:
                    pc.addTrack(self.player.video)

        if self.video_source == VideoSource.CV2:
            for t in pc.getTransceivers():
                if t.kind == "video":
                    pc.addTrack(self.cv2_track)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        response = webrtc_streaming_pb2_pb2.SDP(
            sdp=pc.localDescription.sdp, type=pc.localDescription.type)
        return response


async def _start_async_server(rtp_video_port, video_source, streaming_service_port):
    server = aio.server()
    server.add_insecure_port("[::]:%s" % streaming_service_port)
    pb2_grpc.add_WebRTC_StreamingServicer_to_server(
        WebRTC_Streaming_Service(rtp_video_port, video_source), server
    )
    await server.start()
    await server.wait_for_termination()


def start(signaling_server, secret_key, video_source, rtp_video_port, streaming_service_port):
    webrtc_streaming_server = "localhost:%s" % streaming_service_port
    args = [signaling_server, webrtc_streaming_server, secret_key]
    t = threading.Thread(
        target=communicate_with_signaling_server, args=args)
    t.start()
    logging.basicConfig()
    loop = asyncio.get_event_loop()
    loop.create_task(_start_async_server(rtp_video_port=rtp_video_port,
                                         video_source=video_source,
                                         streaming_service_port=streaming_service_port))
    loop.run_forever()
