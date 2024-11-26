from typing import Optional, List
import grpc
from letta.schemas.memory import ChatMemory
from pydantic import Field, PrivateAttr

class GrpcMemory(ChatMemory):
    """
    Memory implementation using gRPC for storing and managing person records in a database.
    This class extends ChatMemory to provide database operations through a gRPC connection.

    Attributes:
        _channel (grpc.Channel): Private attribute for gRPC channel connection
        _stub (object): Private attribute for gRPC service stub
        grpc_address (str): The address of the gRPC server (default: "localhost:5055")
    """
    
    # Private attributes for gRPC channel and stub
    _channel: grpc.Channel = PrivateAttr(default=None)
    _stub: object = PrivateAttr(default=None)
    grpc_address: str = Field(default="localhost:5055")

    def __init__(self, human: str, persona: str, grpc_channel: str = 'localhost:5055'):
        """
        Initialize GrpcMemory with gRPC channel connection.

        Args:
            human (str): Name or identifier of the human user
            persona (str): Description of the agent's persona
            grpc_channel (str, optional): gRPC server address. Defaults to 'localhost:5055'
        """
        super().__init__(human=human, persona=persona)
        self.grpc_address = grpc_channel
        self._channel = grpc.insecure_channel(grpc_channel)
        
        # Import proto modules
        try:
            from letta_agents_grpc import multi_service_pb2_grpc as pb2_grpc
        except ImportError:
            import multi_service_pb2_grpc as pb2_grpc
        
        self._stub = pb2_grpc.PersonServiceStub(self._channel)

    def create_person(self, name: str, age: int, location: str) -> Optional[str]:
        """
        Create a new person record in the database.

        Args:
            name (str): The name of the person to create
            age (int): The age of the person
            location (str): The location/address of the person

        Returns:
            Optional[str]: A success message with the created person's ID if successful,
                         or an error message if the creation fails
        """
        try:
            from letta_agents_grpc import multi_service_pb2 as pb2
        except ImportError:
            import multi_service_pb2 as pb2
        import grpc    
        request = pb2.CreatePersonRequest(
            name=name,
            age=age,
            location=location
        )
        try:
            response = self._stub.CreatePerson(request)
            return f"Person created with ID: {response.id}, Message: {response.message}"
        except grpc.RpcError as e:
            return f"Error creating person: {str(e)}"

    def get_person(self, person_id: int) -> Optional[str]:
        """
        Get a person's details by their ID.

        Args:
            person_id (int): The unique identifier of the person to retrieve

        Returns:
            Optional[str]: A formatted string containing the person's details if found,
                         or an error message if the person is not found or retrieval fails
        """
        try:
            from letta_agents_grpc import multi_service_pb2 as pb2
        except ImportError:
            import multi_service_pb2 as pb2
        import grpc    
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
            Optional[str]: A formatted string containing all persons' details if successful,
                         or an error message if the listing fails. Returns "No persons found"
                         if the database is empty.
        """
        try:
            from letta_agents_grpc import multi_service_pb2 as pb2
        except ImportError:
            import multi_service_pb2 as pb2
        import grpc    
        request = pb2.Empty()
        try:
            responses = self._stub.ListPersons(request)
            result = []
            for response in responses:
                person_info = f"Name: {response.name}, Age: {response.age}, Location: {response.location}, ID: {response.id}"
                result.append(person_info)
            return "\n".join(result) if result else "No persons found"
        except grpc.RpcError as e:
            return f"Error listing persons: {str(e)}"

    def delete_person(self, person_id: int) -> Optional[str]:
        """
        Delete a person by their ID.

        Args:
            person_id (int): The unique identifier of the person to delete

        Returns:
            Optional[str]: A success message if the deletion was successful,
                         or an error message if the deletion fails
        """
        try:
            from letta_agents_grpc import multi_service_pb2 as pb2
        except ImportError:
            import multi_service_pb2 as pb2
        import grpc    
        request = pb2.PersonIdRequest(id=person_id)
        try:
            response = self._stub.DeletePersonById(request)
            return f"Delete operation status: {response.status}"
        except grpc.RpcError as e:
            return f"Error deleting person: {str(e)}"

    def __del__(self):
        """Clean up the gRPC channel when the object is destroyed."""
        if hasattr(self, "_channel"):
            self._channel.close()
