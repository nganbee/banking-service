PROTO_FILE = intent_service.proto

all: intent_service_pb2.py

intent_service_pb2.py: $(PROTO_FILE)
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $(PROTO_FILE)

clean:
	rm -f intent_service_pb2.py intent_service_pb2_grpc.py