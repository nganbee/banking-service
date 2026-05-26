import grpc
import sys

# Import generated classes từ thư mục intent_grpc
import intent_service_pb2
import intent_service_pb2_grpc

def test_intent_service(message: str):
    print(f"Bắt đầu kết nối tới gRPC Server...")
    
    try:
        # 1. Tạo một kênh kết nối tới server ở cổng 50051
        channel = grpc.insecure_channel('localhost:50051')
        
        # 2. Khởi tạo stub (client)
        stub = intent_service_pb2_grpc.IntentServiceStub(channel)
        
        # 3. Tạo request object chứa tin nhắn
        print(f"Gửi tin nhắn: '{message}'")
        request = intent_service_pb2.IntentRequest(message=message)
        
        # 4. Gọi hàm IntentRecognizer trên Server (Chờ tối đa 120 giây vì LLM trả lời chậm)
        response = stub.IntentRecognizer(request, timeout=300.0)
        
        # 5. In kết quả trả về
        print("\n✅ KẾT QUẢ TỪ SERVER:")
        print(f"- Ý định (Intent): {response.intent}")
        print(f"- Độ tự tin (Confidence): {response.confidence}")
        print(f"- Lý do (Reason): {response.reason}")
        
    except grpc.RpcError as e:
        print(f"\n❌ LỖI KẾT NỐI: {e.details()}")
        print("Bạn đã chắc chắn chạy 'python server.py' ở một cửa sổ Terminal khác chưa?")

if __name__ == "__main__":
    # Bạn có thể truyền tin nhắn vào qua command line, ví dụ: python client.py "Tôi muốn mở tài khoản"
    # Nếu không truyền gì thì dùng câu mặc định dưới đây.
    test_message = "I want to block my credit card immediately!"
    
    if len(sys.argv) > 1:
        test_message = " ".join(sys.argv[1:])
        
    test_intent_service(test_message)
