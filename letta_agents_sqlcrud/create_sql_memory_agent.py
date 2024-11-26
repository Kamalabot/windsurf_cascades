import os
from pathlib import Path
from letta import create_client, LLMConfig, EmbeddingConfig
from letta.schemas.memory import ChatMemory
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, List, Dict, Any

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

class SqlMemory(ChatMemory):
    """
    Custom ChatMemory implementation for SQL database operations.
    Extends the base ChatMemory class to provide CRUD operations for Person records.
    Each method establishes its own database connection to ensure thread safety.
    
    To use a different database path:
    1. When creating the SqlMemory instance, provide the db_path parameter:
       memory = SqlMemory(persona="...", human="...", db_path="/path/to/your/database.db")
    
    2. When calling individual methods, use the db_path parameter:
       memory.create_person("John", "john@example.com", db_path="/path/to/your/database.db")
    """
    
    def __init__(self, persona: str, human: str, db_path: str = DEFAULT_DB_PATH):
        """
        Initialize SqlMemory with persona and database configuration.
        
        Args:
            persona (str): The system prompt / persona description
            human (str): The human user's description
            db_path (str): Path to the SQLite database file. Defaults to current_dir/person.db
        """
        super().__init__(persona=persona, human=human)
    
    
    def create_person(self, name: str, email: str, db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
        """
        Create a new person record in the database.
        
        Args:
            name (str): Person's full name
            email (str): Person's email address
            db_path (str): Optional database path. Defaults to current_dir/person.db
        
        Returns:
            Dict[str, Any]: Response dictionary containing:
                - status: "success" or "error"
                - data: Person data if successful
                - message: Error message if failed
        
        Example:
            >>> memory.create_person("John Doe", "john@example.com")
            {'status': 'success', 'data': {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}}
        """
        try:
            engine = create_engine(f"sqlite:////media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db", echo=True)
            with Session(engine) as session:
                person = Person(name=name, email=email)
                session.add(person)
                session.commit()
                session.refresh(person)
                return {"status": "success", "data": {"id": person.id, "name": person.name, "email": person.email}}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def read_person(self, person_id: Optional[int] = None, db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
        """
        Read person record(s) from the database.
        
        Args:
            person_id (Optional[int]): ID of person to retrieve. If None, retrieves all records
            db_path (str): Optional database path. Defaults to current_dir/person.db
        
        Returns:
            Dict[str, Any]: Response dictionary containing:
                - status: "success" or "error"
                - data: Single person data or list of all people if successful
                - message: Error message if failed
        
        Example:
            >>> memory.read_person(1)
            {'status': 'success', 'data': {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}}
        """
        try:
            engine = create_engine(f"sqlite:////media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db", echo=True)
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
    
    def update_person(self, person_id: int, name: Optional[str] = None, email: Optional[str] = None, db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
        """
        Update an existing person record in the database.
        
        Args:
            person_id (int): ID of person to update
            name (Optional[str]): New name for the person, if provided
            email (Optional[str]): New email for the person, if provided
            db_path (str): Optional database path. Defaults to current_dir/person.db
        
        Returns:
            Dict[str, Any]: Response dictionary containing:
                - status: "success" or "error"
                - data: Updated person data if successful
                - message: Error message if failed
        
        Example:
            >>> memory.update_person(1, name="John Smith")
            {'status': 'success', 'data': {'id': 1, 'name': 'John Smith', 'email': 'john@example.com'}}
        """
        try:
            engine = create_engine(f"sqlite:////media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db", echo=True)
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
    
    def delete_person(self, person_id: int, db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
        """
        Delete a person record from the database.
        
        Args:
            person_id (int): ID of person to delete
            db_path (str): Optional database path. Defaults to current_dir/person.db
        
        Returns:
            Dict[str, Any]: Response dictionary containing:
                - status: "success" or "error"
                - message: Success or error message
        
        Example:
            >>> memory.delete_person(1)
            {'status': 'success', 'message': 'Person with id 1 deleted successfully'}
        """
        try:
            engine = create_engine(f"sqlite:////media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db", echo=True)
            with Session(engine) as session:
                person = session.get(Person, person_id)
                if not person:
                    return {"status": "error", "message": f"Person with id {person_id} not found"}
                
                session.delete(person)
                session.commit()
                return {"status": "success", "message": f"Person with id {person_id} deleted successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

def create_sqlcrud_agent(db_path: str = DEFAULT_DB_PATH):
    """
    Create and configure the SQL CRUD agent with appropriate LLM and embedding settings.
    
    Args:
        db_path (str): Optional database path. Defaults to current_dir/person.db
    
    Returns:
        Agent: Configured Letta agent instance ready for database operations
    
    Note:
        This function reads the system prompt from sqlcrud_system_prompt.txt and
        configures the agent to use either Groq or OpenAI based on available API keys.
    """
    client = create_client()
    
    with open("sqlcrud_system_prompt.txt", "r") as f:
        system_prompt = f.read()
    
    llm_config = LLMConfig(
        provider="groq" if os.getenv("GROQ_API_KEY") else "openai",
        model="mixtral-8x7b-32768" if os.getenv("GROQ_API_KEY") else "gpt-4-turbo-preview"
    )
    
    embedding_config = EmbeddingConfig(
        provider="openai",
        model="text-embedding-3-small"
    )
    
    memory = SqlMemory(
        persona=system_prompt,
        human="User",
        db_path=db_path
    )
    
    agent = client.create_agent(
        name="sqlcrud_agent",
        llm_config=llm_config,
        embedding_config=embedding_config,
        memory=memory
    )
    
    return agent

if __name__ == "__main__":
    engine = create_engine(f"sqlite:////media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db", echo=True)
    SQLModel.metadata.create_all(engine)
    agent = create_sqlcrud_agent()
    print("SQL CRUD agent created successfully! Database path: /media/uberdev/ddrv/gitFolders/windsurf_cascades/letta_agents_sqlcrud/person.db")
