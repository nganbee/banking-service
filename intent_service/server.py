import grpc
from concurrent import futures
import time

# Import generated classes
import intent_service_pb2
import intent_service_pb2_grpc

# Import class phân loại từ node bạn đã viết sẵn
from app.nodes.intent_node import classifier

class IntentServiceServicer(intent_service_pb2_grpc.IntentServiceServicer):
    def IntentRecognizer(self, request, context):
        print(f"--> [IntentServer] Received message: {request.message}")
        
        intent, confidence = classifier.predict(request.message)
        
        reason = f"Logprob Confidence: {confidence}"
        
        print(f"<-- [IntentServer] Predicted: {intent} (Confidence: {confidence})")
        return intent_service_pb2.IntentResponse(
            intent=intent,
            confidence=confidence,
            reason=reason
        )

def serve():
    # Khởi tạo gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    intent_service_pb2_grpc.add_IntentServiceServicer_to_server(IntentServiceServicer(), server)
    
    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"[START] Intent gRPC Server is running on port {port}...")
    
    try:
        # Keep server alive
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
