from typing import Optional, List
import grpc
from letta.schemas.memory import ChatMemory
from pydantic import Field, PrivateAttr
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    import multi_service_pb2 as pb2
    import multi_service_pb2_grpc as pb2_grpc
except ImportError as e:
    print(f"Error importing proto modules: {e}")
    print(f"Python path: {sys.path}")
    raise

class GrpcMemory(ChatMemory):
    _channel: grpc.Channel = PrivateAttr(default=None)
    _stub: pb2_grpc.PersonServiceStub = PrivateAttr(default=None)
    grpc_address: str = Field(default="localhost:5055")

    def __init__(self, human: str, persona: str, grpc_channel: str = 'localhost:5055'):
        """
        Initialize GrpcMemory with gRPC channel connection.
        
        Args:
            human (str): Human context for the chat memory
            persona (str): Persona context for the chat memory
            grpc_channel (str): gRPC channel address (default: localhost:5055)
        """
        super().__init__(human=human, persona=persona)
        self.grpc_address = grpc_channel
        self._channel = grpc.insecure_channel(grpc_channel)
        self._stub = pb2_grpc.PersonServiceStub(self._channel)
        
    def create_person(self, name: str, age: int, location: str) -> Optional[str]:
        """
        Create a new person record in the database.
        
        Args:
            name (str): Name of the person
            age (int): Age of the person
            location (str): Location of the person
            
        Returns:
            Optional[str]: Response message with the created person's ID
        """
        request = pb2.CreatePersonRequest(
            name=name,
            age=age,
            location=location
        )
        try:
            response = self._stub.CreatePerson(request)
            return f"Person created successfully with ID: {response.id}. {response.message}"
        except grpc.RpcError as e:
            return f"Error creating person: {str(e)}"

    def get_person(self, person_id: int) -> Optional[str]:
        """
        Retrieve a person's details by their ID.
        
        Args:
            person_id (int): ID of the person to retrieve
            
        Returns:
            Optional[str]: Person's details if found, error message if not found
        """
        request = pb2.PersonIdRequest(id=person_id)
        try:
            response = self._stub.GetPersonById(request)
            return f"Person found - Name: {response.name}, Age: {response.age}, Location: {response.location}, ID: {response.id}"
        except grpc.RpcError as e:
            return f"Error retrieving person: {str(e)}"

    def list_persons(self) -> Optional[str]:
        """
        List all persons in the database.
        
        Returns:
            Optional[str]: List of all persons' details
        """
        request = pb2.Empty()
        try:
            responses = self._stub.ListPersons(request)
            result = []
            for response in responses:
                person_info = f"Name: {response.name}, Age: {response.age}, Location: {response.location}, ID: {response.id}"
                result.append(person_info)
            return "\n".join(result) if result else "No persons found in the database"
        except grpc.RpcError as e:
            return f"Error listing persons: {str(e)}"

    def delete_person(self, person_id: int) -> Optional[str]:
        """
        Delete a person from the database by their ID.
        
        Args:
            person_id (int): ID of the person to delete
            
        Returns:
            Optional[str]: Status message indicating success or failure
        """
        request = pb2.PersonIdRequest(id=person_id)
        try:
            response = self._stub.DeletePersonById(request)
            return f"Delete operation status: {response.status}"
        except grpc.RpcError as e:
            return f"Error deleting person: {str(e)}"

    def __del__(self):
        """
        Clean up the gRPC channel when the object is destroyed.
        """
        if hasattr(self, '_channel'):
            self._channel.close()
