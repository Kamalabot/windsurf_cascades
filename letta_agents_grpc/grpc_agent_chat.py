import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from letta import create_client, LLMConfig, EmbeddingConfig
from grpc_memory import GrpcMemory


class GrpcAgentChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Agent Chat Interface")
        self.root.geometry("800x600")

        # Initialize agent state to None
        self.agent_state = None
        self.client = None

        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        # Create main containers
        self.create_chat_frame()
        self.create_database_frame()

        # Initialize Letta client and agent
        self.initialize_agent()

    def create_chat_frame(self):
        """Create the chat interface frame"""
        chat_frame = ttk.Frame(self.root)
        chat_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Configure chat frame grid
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(1, weight=0)
        chat_frame.grid_columnconfigure(0, weight=1)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, height=20
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Message input frame
        input_frame = ttk.Frame(chat_frame)
        input_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)

        self.message_input = ttk.Entry(input_frame)
        self.message_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_button.grid(row=0, column=1)

        # Bind Enter key to send message
        self.message_input.bind("<Return>", lambda e: self.send_message())

    def create_database_frame(self):
        """Create the database operations frame"""
        db_frame = ttk.LabelFrame(self.root, text="Database Operations")
        db_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Quick actions
        ttk.Button(
            db_frame,
            text="List All Records",
            command=lambda: self.send_message("Show all records"),
        ).pack(fill="x", padx=5, pady=2)

        # Add Person Frame
        add_frame = ttk.LabelFrame(db_frame, text="Add Person")
        add_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(add_frame, text="Name:").pack(anchor="w", padx=5)
        self.name_entry = ttk.Entry(add_frame)
        self.name_entry.pack(fill="x", padx=5)

        ttk.Label(add_frame, text="Age:").pack(anchor="w", padx=5)
        self.age_entry = ttk.Entry(add_frame)
        self.age_entry.pack(fill="x", padx=5)

        ttk.Label(add_frame, text="Location:").pack(anchor="w", padx=5)
        self.location_entry = ttk.Entry(add_frame)
        self.location_entry.pack(fill="x", padx=5)

        ttk.Button(add_frame, text="Add Person", command=self.add_person).pack(
            fill="x", padx=5, pady=5
        )

        # Get/Delete Person Frame
        action_frame = ttk.LabelFrame(db_frame, text="Get/Delete Person")
        action_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(action_frame, text="Person ID:").pack(anchor="w", padx=5)
        self.id_entry = ttk.Entry(action_frame)
        self.id_entry.pack(fill="x", padx=5)

        button_frame = ttk.Frame(action_frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(button_frame, text="Get Person", command=self.get_person).pack(
            side="left", expand=True, padx=2
        )
        ttk.Button(button_frame, text="Delete Person", command=self.delete_person).pack(
            side="left", expand=True, padx=2
        )

    def initialize_agent(self):
        """Initialize the Letta client with custom memory"""
        try:
            self.display_message("System", "Starting agent initialization...")

            # Create Letta client
            self.client = create_client()
            self.display_message("System", "Letta client created!")

            # Configure LLM with OpenAI
            llm_config = LLMConfig(
                model="gpt-4-0125-preview",  # Using GPT-4 Turbo
                model_endpoint_type="openai",
                model_endpoint="https://api.openai.com/v1",
                context_window=128000,
                put_inner_thoughts_in_kwargs=True,
            )

            # Configure embeddings with OpenAI
            embedding_config = EmbeddingConfig(
                embedding_endpoint_type="openai",
                embedding_endpoint="https://api.openai.com/v1",
                embedding_model="text-embedding-ada-002",
                embedding_dim=1536,
                embedding_chunk_size=300
            )
            self.display_message("System", "AI configurations ready!")

            # Simple memory initialization
            memory = GrpcMemory(human="user", persona="assistant")
            self.display_message("System", "Memory configuration ready!")

            # Try to get existing agent, create new one if it doesn't exist
            try:
                self.agent_state = self.client.get_agent_by_name("db_agent")
                if self.agent_state:
                    self.display_message("System", "Successfully connected to existing database agent!")
                    return
            except Exception:
                self.display_message("System", "Creating new database agent...")
                # Create the agent with detailed system prompt
                self.agent_state = self.client.create_agent(
                    name="db_agent",
                    system="""I am a database administrator assistant specialized in managing a person database. I can help you with:

                    1. Creating Person Records:
                       - Add new persons with their name, age, and location
                       - Validate input data before creation
                       - Provide feedback on successful creation

                    2. Retrieving Information:
                       - Get person details by their ID
                       - List all persons in the database
                       - Format results in a clear, readable manner

                    3. Database Management:
                       - Delete person records by ID
                       - Maintain data consistency
                       - Provide clear status updates

                    I will always:
                    - Confirm successful operations
                    - Provide clear error messages when something goes wrong
                    - Format responses in a user-friendly way
                    - Guide you through the correct usage of commands

                    Please provide clear instructions, and I'll help you manage the database efficiently.""",
                    memory=memory,
                    embedding_config=embedding_config,
                    llm_config=llm_config,
                )
                self.display_message("System", "New database agent created successfully!")

        except Exception as e:
            self.display_message(
                "System Error", f"Failed to initialize agent: {str(e)}"
            )
            if hasattr(e, "__cause__"):
                self.display_message("System Error", f"Caused by: {str(e.__cause__)}")

    def send_message(self, message=None):
        """Send a message to the agent"""
        if not self.agent_state:
            self.display_message("System Error", "Agent not initialized. Please wait for initialization or restart the application.")
            return

        if message is None:
            message = self.message_input.get()

        if message.strip():
            # Display user message
            self.display_message("User", message)
            self.message_input.delete(0, tk.END)

            # Process agent response in a separate thread
            thread = threading.Thread(
                target=self.process_agent_response, args=(message,)
            )
            thread.start()

    def process_agent_response(self, message):
        """Process the agent's response in a separate thread"""
        if not self.agent_state:
            self.root.after(0, self.display_message, "System Error", "Agent not initialized")
            return

        try:
            response = self.client.send_message(
                agent_id=self.agent_state.id, role="user", message=message
            )

            self.root.after(0, self.display_message, "Agent", response)

        except Exception as e:
            error_msg = f"Error getting response: {str(e)}"
            if hasattr(e, "__cause__") and e.__cause__:
                error_msg += f"\nCaused by: {str(e.__cause__)}"
            self.root.after(
                0,
                self.display_message,
                "System Error",
                error_msg,
            )

    def display_message(self, sender, message):
        """Display a message in the chat window"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, f"\n{sender}: {message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see(tk.END)

    def add_person(self):
        """Add a person using the form data"""
        if not self.agent_state:
            self.display_message("System Error", "Agent not initialized. Please wait for initialization or restart the application.")
            return

        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        location = self.location_entry.get().strip()

        if name and age and location:
            try:
                age = int(age)
                message = f"Create a new person with name: {name}, age: {age}, and location: {location}"
                self.send_message(message)
                
                # Clear the form
                self.name_entry.delete(0, tk.END)
                self.age_entry.delete(0, tk.END)
                self.location_entry.delete(0, tk.END)
            except ValueError:
                self.display_message("System Error", "Age must be a valid number")
        else:
            self.display_message("System Error", "Please fill in all fields")

    def get_person(self):
        """Get person details by ID"""
        if not self.agent_state:
            self.display_message("System Error", "Agent not initialized. Please wait for initialization or restart the application.")
            return

        person_id = self.id_entry.get().strip()
        if person_id:
            try:
                person_id = int(person_id)
                message = f"Get person with ID: {person_id}"
                self.send_message(message)
            except ValueError:
                self.display_message("System Error", "ID must be a valid number")
        else:
            self.display_message("System Error", "Please enter a person ID")

    def delete_person(self):
        """Delete person by ID"""
        if not self.agent_state:
            self.display_message("System Error", "Agent not initialized. Please wait for initialization or restart the application.")
            return

        person_id = self.id_entry.get().strip()
        if person_id:
            try:
                person_id = int(person_id)
                message = f"Delete person with ID: {person_id}"
                self.send_message(message)
                self.id_entry.delete(0, tk.END)
            except ValueError:
                self.display_message("System Error", "ID must be a valid number")
        else:
            self.display_message("System Error", "Please enter a person ID")


def main():
    root = tk.Tk()
    app = GrpcAgentChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
