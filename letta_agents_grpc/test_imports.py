#!/usr/bin/env python3

import os
import sys
import grpc
import time

def test_proto_imports():
    """Test proto file imports"""
    try:
        print("\n1. Testing Proto Imports...")
        import multi_service_pb2 as pb2
        import multi_service_pb2_grpc as pb2_grpc
        print("✓ Successfully imported proto modules!")
        return pb2, pb2_grpc
    except Exception as e:
        print("✗ Failed to import proto modules:")
        print(f"Error: {str(e)}")
        raise

def test_grpc_connection(pb2, pb2_grpc):
    """Test gRPC server connection"""
    print("\n2. Testing gRPC Server Connection...")
    
    # Create channel and stub
    channel = grpc.insecure_channel('localhost:5055')
    stub = pb2_grpc.PersonServiceStub(channel)
    
    try:
        # Test connection with a simple ListPersons request
        request = pb2.Empty()
        # Set a timeout of 5 seconds
        responses = stub.ListPersons(request, timeout=5)
        # Try to get the first response (if any)
        next(responses, None)
        print("✓ Successfully connected to gRPC server!")
        return channel, stub
    except grpc.RpcError as e:
        print("✗ Failed to connect to gRPC server:")
        print(f"  - Status: {e.code()}")
        print(f"  - Details: {e.details()}")
        channel.close()
        raise
    except Exception as e:
        print("✗ Unexpected error:")
        print(f"  - {str(e)}")
        channel.close()
        raise

def test_list_persons(stub, pb2):
    """Test ListPersons service"""
    print("\n3. Testing ListPersons Service...")
    try:
        request = pb2.Empty()
        responses = stub.ListPersons(request)
        print("✓ ListPersons request successful!")
        print("\nPerson Records:")
        print("-" * 50)
        count = 0
        for response in responses:
            count += 1
            print(f"Person {count}:")
            print(f"  - ID: {response.id}")
            print(f"  - Name: {response.name}")
            print(f"  - Age: {response.age}")
            print(f"  - Location: {response.location}")
            print("-" * 50)
        if count == 0:
            print("No person records found in database.")
    except grpc.RpcError as e:
        print("✗ ListPersons request failed:")
        print(f"  - Status: {e.code()}")
        print(f"  - Details: {e.details()}")
        raise

def main():
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    try:
        # Test proto imports
        pb2, pb2_grpc = test_proto_imports()
        
        # Test gRPC connection
        channel, stub = test_grpc_connection(pb2, pb2_grpc)
        
        # Test ListPersons service
        test_list_persons(stub, pb2)
        
        # Clean up
        channel.close()
        print("\n✓ All tests completed successfully!")
        
    except Exception as e:
        print("\n✗ Tests failed!")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
