import grpc
from typing import Tuple

from app.clients.intent_grpc import intent_service_pb2
from app.clients.intent_grpc import intent_service_pb2_grpc

class GrpcIntentClient:
    def __init__(self, host: str = "localhost", port: int = 50051):
        # Open channel to gRPC server
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        # Create stub
        self.stub = intent_service_pb2_grpc.IntentServiceStub(self.channel)
        
    def predict_intent(self, message: str) -> Tuple[str, float, str]:
        """
        Request to Intent gRPC Service return intent, confidence, reason.
        """
        try:
            request = intent_service_pb2.IntentRequest(message=message)

            response = self.stub.IntentRecognizer(request, timeout=10.0)
            
            return response.intent, response.confidence, response.reason
            
        except grpc.RpcError as e:
            print(f"gRPC call failed: {e}")
            # Fallback
            return "unknown", 0.0, f"gRPC Error: {e.details()}"

    def close(self):
        self.channel.close()

grpc_intent_client = GrpcIntentClient()
