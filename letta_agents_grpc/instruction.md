# Letta Agents gRPC Project

## Project Details

This project implements a gRPC-based communication layer for the Letta Agents framework. Letta is a Python framework that provides a declarative approach to building agents, enabling complex interactions between agents and systems.

### Key Components

1. **gRPC Service Definitions**
   - Protocol Buffer definitions for Person Database
   - Python gRPC stub and service implementations
   - Message types for data exchange

2. **Agent Communication**
   - Build custom GrpcMemory that extends ChatMemory from Letta frarmework
   - Custom methods for interacting with gRPC service from the agent, which will be tools for the agent

3. **Framework Integration**
   - Seamless integration with existing Letta Agents
   - Extension points for custom agent behaviors
   - Standardized communication patterns

### Project Structure

```
letta_agents_grpc/
├── instruction.md                # Project documentation
├── requirements.txt             # Project dependencies
├── multi_service.proto          # Protocol Buffer service definitions
├── multi_service_pb2.py         # Generated Protocol Buffer code
├── multi_service_pb2_grpc.py    # Generated gRPC code
├── person.py                    # Database model definition
├── grpc_memory.py              # Custom memory implementation for gRPC
├── grpc_agent_chat.py          # Tkinter GUI for database agent
├── grpc_dbcrud_system_prompt.txt # System prompt for database operations
└── task_queue_system_prompt.txt  # Reference system prompt
```

### Getting Started

- Firstneed to install letta in your machine. 
- Then execute letta server which will by default launch a Letta Server, on http://localhost:8283
- Create the GrpcMemory for the agent, which can be used as memory for the agent, and it can perform crud operations on the attached database.
- Create the grpc_system_prompt.txt for the agent, refering to the task_queue_system_prompt.txt   

- Create a client to connect to the Letta Server base on the example provided in the Development Guidelines

### Development Guidelines

Example Code to connect with Letta Server

```
from letta import create_client, LLMConfig, EmbeddingConfig
from letta.schemas.memory import ChatMemory

client = create_client()

# Using the groq_models, need to configure groq api keys
# refer to the process here https://docs.letta.com/models/groq

tool_llm = LLMConfig(model="llama3-groq-8b-8192-tool-use-preview", model_endpoint_type='groq', model_endpoint='https://api.groq.com/openai/v1', model_wrapper=None, context_window=8192, put_inner_thoughts_in_kwargs=True)
hf_embed = EmbeddingConfig(embedding_model="letta-free", embedding_endpoint_type="hugging-face", embedding_dim=1024, embedding_chunk_size=300, embedding_endpoint="https://embeddings.memgpt.ai")

memory_blocks = ChatMemory(
    human="Call me Superman",
    persona="I am a super Intelligent being"
)

# Agent Instances is created in Python
# In the Letta Server, the Agent will be created

tooluser_state = client.create_agent(
    name="tooluser",
    system=open("data/main_system_prompt.txt", "r").read(),
    memory=memory_blocks,
    embedding_config=hf_embed,
    llm_config=tool_llm
)

# Sending message to the Agent, and getting response
response = client.send_message(
    agent_id=tagentstate.id,
    role="user",
    message="Add 'get me a contact of POTUS' and 'call me TaskMaster'",
)

response
```

Example code to create a custom ChatMemory based on the Letta's ChatMemory
https://docs.letta.com/advanced/custom_memory

Below is an example of how to create a custom ChatMemory, where the task queue is stored in core memory, and the agent can push and pop tasks from the queue.

```
from letta.memory import ChatMemory, MemoryModule
from typing import Optional, List

class TaskMemory(ChatMemory): 

    def __init__(self, human: str, persona: str, tasks: List[str]): 
        super().__init__(human=human, persona=persona) 
        self.memory["tasks"] = MemoryModule(limit=2000, value=tasks) # create an empty list 


    
    def task_queue_push(self, task_description: str) -> Optional[str]:
        """
        Push to a task queue stored in core memory. 

        Args:
            task_description (str): A description of the next task you must accomplish. 
            
        Returns:
            Optional[str]: None is always returned as this function does not produce a response.
        """
        self.memory["tasks"].value.append(task_description)
        return None

    def task_queue_pop(self) -> Optional[str]:
        """
        Get the next task from the task queue 
 
        Returns:
            Optional[str]: The description of the task popped from the queue, 
            if there are still tasks in queue. Otherwise, returns None (the 
            task queue is empty)
        """
        if len(self.memory["tasks"].value) == 0: 
            return None
        task = self.memory["tasks"].value[0]
        self.memory["tasks"].value = self.memory["tasks"].value[1:]
        return task

task_agent_state = client.create_agent(
    name="task_agent", 
    memory=TaskMemory(
        human="My name is Sarah", 
        persona="You have an additional section of core memory called `tasks`. " \
        + "This section of memory contains of list of tasks you must do." \
        + "Use the `task_queue_push` tool to write down tasks so you don't forget to do them." \
        + "If there are tasks in the task queue, you should call `task_queue_pop` to retrieve and remove them. " \
        + "Keep calling `task_queue_pop` until there are no more tasks in the queue. " \
        + "Do *not* call `send_message` until you have completed all tasks in your queue. " \
        + "If you call `task_queue_pop`, you must always do what the popped task specifies", 
        tasks=["start calling yourself Bob", "tell me a haiku with my name"], 
    )
)

```
ChatMemory implementation for reference

```
from memgpt.memory import BaseMemory

class ChatMemory(BaseMemory):

    def __init__(self, persona: str, human: str, limit: int = 2000):
        self.memory = {
            "persona": MemoryModule(name="persona", value=persona, limit=limit),
            "human": MemoryModule(name="human", value=human, limit=limit),
        }

    def core_memory_append(self, name: str, content: str) -> Optional[str]:
        """
        Append to the contents of core memory.

        Args:
            name (str): Section of the memory to be edited (persona or human).
            content (str): Content to write to the memory. All unicode (including emojis) are supported.

        Returns:
            Optional[str]: None is always returned as this function does not produce a response.
        """
        self.memory[name].value += "\n" + content
        return None

    def core_memory_replace(self, name: str, old_content: str, new_content: str) -> Optional[str]:
        """
        Replace the contents of core memory. To delete memories, use an empty string for new_content.

        Args:
            name (str): Section of the memory to be edited (persona or human).
            old_content (str): String to replace. Must be an exact match.
            new_content (str): Content to write to the memory. All unicode (including emojis) are supported.

        Returns:
            Optional[str]: None is always returned as this function does not produce a response.
        """
        self.memory[name].value = self.memory[name].value.replace(old_content, new_content)
        return None
