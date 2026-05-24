import grpc
from typing import Tuple

from app.clients.intent_grpc import intent_service_pb2
from app.clients.intent_grpc import intent_service_pb2_grpc

class GrpcIntentClient:
    def __init__(self, host: str = "localhost", port: int = 50051):
        # Mở một channel (không mã hóa) tới gRPC server
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        # Khởi tạo stub để thực hiện việc gọi RPC
        self.stub = intent_service_pb2_grpc.IntentServiceStub(self.channel)
        
    def predict_intent(self, message: str) -> Tuple[str, float, str]:
        """
        Gửi yêu cầu tới Intent gRPC Service và trả về intent, confidence, reason.
        """
        try:
            # Gói message vào Request Object đã định nghĩa trong proto
            request = intent_service_pb2.IntentRequest(message=message)
            
            # Gọi hàm IntentRecognizer trên Server
            response = self.stub.IntentRecognizer(request, timeout=10.0)
            
            # Trả về cả 3 biến
            return response.intent, response.confidence, response.reason
            
        except grpc.RpcError as e:
            print(f"gRPC call failed: {e}")
            # Xử lý fallback nếu server sập
            return "unknown", 0.0, f"gRPC Error: {e.details()}"

    def close(self):
        self.channel.close()

# Khởi tạo singleton để dùng chung trong app
grpc_intent_client = GrpcIntentClient()
