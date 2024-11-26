import os
from pathlib import Path
from letta import create_client, LLMConfig, EmbeddingConfig
from letta.schemas.memory import ChatMemory
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, List, Dict, Any


class Person(SQLModel, table=True, extend_existing=True):
    """
    SQLModel class representing a person in the database.
    
    Attributes:
        id (Optional[int]): Primary key, auto-incrementing identifier
        name (str): Person's full name
        email (str): Person's email address
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

class SqlMemory(ChatMemory):
    """
    Custom ChatMemory implementation for SQL database operations.
    Extends the base ChatMemory class to provide CRUD operations for Person records.
    Each method establishes its own database connection to ensure thread safety.
    """
    
    def __init__(self, persona: str, human: str):
        """
        Initialize SqlMemory with persona and database configuration.
        
        Args:
            persona (str): The system prompt / persona description
            human (str): The human user's description
        
        Returns:
            None
        """
        super().__init__(persona=persona, human=human)
    
    def create_person(self, name: str, email: str):
        """
        Create a new person record in the database.
        
        Args:
            name (str): Person's full name
            email (str): Person's email address
        
        Returns:
            Response dictionary containing:
                - status (str): "success" or "error"
                - data : Person data if successful
                - message (str): Error message if failed
        
        Example:
            >>> memory.create_person("John Doe", "john@example.com")
            {'status': 'success', 'data': {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}}
        """
        from sqlmodel import SQLModel, Field, Session, select, create_engine
        from typing import Optional

        # Clear existing metadata before defining model
        SQLModel.metadata.clear()
        
        class Person(SQLModel, table=True):
            """
            SQLModel class representing a person in the database.
    
            Attributes:
                id (Optional[int]): Primary key, auto-incrementing identifier
                name (str): Person's full name
                email (str): Person's email address
            """
            id: Optional[int] = Field(default=None, primary_key=True)
            name: str
            email: str
        try:
            # Define the default database path
            DEFAULT_DB_PATH = "/media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db"
            engine = create_engine(f"sqlite:///{DEFAULT_DB_PATH}", echo=True)
            with Session(engine) as session:
                person = Person(name=name, email=email)
                session.add(person)
                session.commit()
                session.refresh(person)
                return {"status": "success", "data": {"id": person.id, "name": person.name, "email": person.email}}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def read_person(self, person_id: Optional[int] = None):
        """
        Read person record(s) from the database.
        
        Args:
            person_id (Optional[int]): ID of person to retrieve. If None, retrieves all records
        
        Returns:
            Response dictionary containing:
                - status (str): "success" or "error"
                - data : Single person data or list of all people if successful
                - message (str): Error message if failed
        
        Example:
            >>> memory.read_person(1)
            {'status': 'success', 'data': {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}}
        """
        from sqlmodel import SQLModel, Field, Session, select, create_engine
        from typing import Optional

        # Clear existing metadata before defining model
        SQLModel.metadata.clear()
        
        class Person(SQLModel, table=True):
            """
            SQLModel class representing a person in the database.
    
            Attributes:
                id (Optional[int]): Primary key, auto-incrementing identifier
                name (str): Person's full name
                email (str): Person's email address
            """
            id: Optional[int] = Field(default=None, primary_key=True)
            name: str
            email: str
        try:
            # Define the default database path
            DEFAULT_DB_PATH = "/media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db"
            engine = create_engine(f"sqlite:///{DEFAULT_DB_PATH}", echo=True)
            with Session(engine) as session:
                if person_id:
                    person = session.get(Person, person_id)
                    if not person:
                        return {"status": "error", "message": f"Person with id {person_id} not found"}
                    return {"status": "success", "data": {"id": person.id, "name": person.name, "email": person.email}}
                else:
                    people = session.exec(select(Person)).all()
                    return {"status": "success", "data": [{"id": p.id, "name": p.name, "email": p.email} for p in people]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_person(self, person_id: int, name: Optional[str] = None, email: Optional[str] = None):
        """
        Update an existing person record in the database.
        
        Args:
            person_id (int): ID of person to update
            name (Optional[str]): New name for the person, if provided
            email (Optional[str]): New email for the person, if provided
        
        Returns:
            Response dictionary containing:
                - status (str): "success" or "error"
                - data : Updated person data if successful
                - message (str): Error message if failed
        
        Example:
            >>> memory.update_person(1, name="John Smith")
            {'status': 'success', 'data': {'id': 1, 'name': 'John Smith', 'email': 'john@example.com'}}
        """
        from sqlmodel import SQLModel, Field, Session, select, create_engine
        from typing import Optional

        # Clear existing metadata before defining model
        SQLModel.metadata.clear()
        
        class Person(SQLModel, table=True):
            """
            SQLModel class representing a person in the database.
    
            Attributes:
                id (Optional[int]): Primary key, auto-incrementing identifier
                name (str): Person's full name
                email (str): Person's email address
            """
            id: Optional[int] = Field(default=None, primary_key=True)
            name: str
            email: str
        try:
            # Define the default database path
            DEFAULT_DB_PATH = "/media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db"
            engine = create_engine(f"sqlite:///{DEFAULT_DB_PATH}", echo=True)
            with Session(engine) as session:
                person = session.get(Person, person_id)
                if not person:
                    return {"status": "error", "message": f"Person with id {person_id} not found"}
                
                if name:
                    person.name = name
                if email:
                    person.email = email
                
                session.add(person)
                session.commit()
                session.refresh(person)
                return {"status": "success", "data": {"id": person.id, "name": person.name, "email": person.email}}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def delete_person(self, person_id: int):
        """
        Delete a person record from the database.
        
        Args:
            person_id (int): ID of person to delete
        
        Returns:
            Response dictionary containing:
                - status (str): "success" or "error"
                - message (str): Success or error message
        
        Example:
            >>> memory.delete_person(1)
            {'status': 'success', 'message': 'Person with id 1 deleted successfully'}
        """
        from sqlmodel import SQLModel, Field, Session, select, create_engine
        from typing import Optional

        # Clear existing metadata before defining model
        SQLModel.metadata.clear()
        
        class Person(SQLModel, table=True):
            """
            SQLModel class representing a person in the database.

            Attributes:
                id (Optional[int]): Primary key, auto-incrementing identifier
                name (str): Person's full name
                email (str): Person's email address
            """
            id: Optional[int] = Field(default=None, primary_key=True)
            name: str
            email: str
        try:
            # Define the default database path
            DEFAULT_DB_PATH = "/media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db"
            engine = create_engine(f"sqlite:///{DEFAULT_DB_PATH}", echo=True)
            with Session(engine) as session:
                person = session.get(Person, person_id)
                if not person:
                    return {"status": "error", "message": f"Person with id {person_id} not found"}
                
                session.delete(person)
                session.commit()
                return {"status": "success", "message": f"Person with id {person_id} deleted successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

def create_sqlcrud_agent():
    """
    Create and configure the SQL CRUD agent with appropriate LLM and embedding settings.
    
    Returns:
        Agent: Configured Letta agent instance ready for database operations
    
    Note:
        This function reads the system prompt from sqlcrud_system_prompt.txt and
        configures the agent to use OpenAI models for both LLM and embeddings.
    """
    client = create_client()
    
    with open("sqlcrud_system_prompt.txt", "r") as f:
        system_prompt = f.read()
    
    llm_config = LLMConfig(
        model="gpt-4o-mini",
        model_endpoint_type="openai",
        model_endpoint="https://api.openai.com/v1",
        context_window=128000
    )
    
    embedding_config = EmbeddingConfig(
        embedding_endpoint_type="openai",
        embedding_endpoint="https://api.openai.com/v1",
        embedding_model="text-embedding-ada-002",
        embedding_dim=1536,
        embedding_chunk_size=300
    )
    
    memory = SqlMemory(persona=system_prompt, human="Human User")
    
    return client.create_agent(
        llm_config=llm_config,
        embedding_config=embedding_config,
        memory=memory
    )

if __name__ == "__main__":
     # Define the default database path
    DEFAULT_DB_PATH = "/media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db"

    # Create database and tables
    engine = create_engine(f"sqlite:///{DEFAULT_DB_PATH}", echo=True)
    SQLModel.metadata.create_all(engine)
    
    # Create and initialize agent
    agent = create_sqlcrud_agent()
    print("SQL CRUD Agent initialized successfully!")
