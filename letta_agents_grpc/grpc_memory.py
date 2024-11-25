from typing import Optional, List
import grpc
from letta.memory import ChatMemory, MemoryModule

import multi_service_pb2
import multi_service_pb2_grpc

class GrpcMemory(ChatMemory):
    def __init__(self, human: str, persona: str, grpc_channel: str = 'localhost:50051'):
        """
        Initialize GrpcMemory with gRPC channel connection.
        
        Args:
            human (str): Human context for the chat memory
            persona (str): Persona context for the chat memory
            grpc_channel (str): gRPC channel address (default: localhost:50051)
        """
        super().__init__(human=human, persona=persona)
        self.channel = grpc.insecure_channel(grpc_channel)
        self.stub = multi_service_pb2_grpc.PersonServiceStub(self.channel)
        
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
        request = multi_service_pb2.CreatePersonRequest(
            name=name,
            age=age,
            location=location
        )
        try:
            response = self.stub.CreatePerson(request)
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
        request = multi_service_pb2.PersonIdRequest(id=person_id)
        try:
            response = self.stub.GetPersonById(request)
            return f"Person found - Name: {response.name}, Age: {response.age}, Location: {response.location}, ID: {response.id}"
        except grpc.RpcError as e:
            return f"Error retrieving person: {str(e)}"

    def list_persons(self) -> Optional[str]:
        """
        List all persons in the database.
        
        Returns:
            Optional[str]: List of all persons' details
        """
        request = multi_service_pb2.Empty()
        try:
            responses = self.stub.ListPersons(request)
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
        request = multi_service_pb2.PersonIdRequest(id=person_id)
        try:
            response = self.stub.DeletePersonById(request)
            return f"Delete operation status: {response.status}"
        except grpc.RpcError as e:
            return f"Error deleting person: {str(e)}"

    def __del__(self):
        """
        Clean up the gRPC channel when the object is destroyed.
        """
        if hasattr(self, 'channel'):
            self.channel.close()
