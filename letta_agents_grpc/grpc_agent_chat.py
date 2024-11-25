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
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=20)
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
        ttk.Button(db_frame, text="List All Records", 
                  command=lambda: self.send_message("Show all records")).pack(fill="x", padx=5, pady=2)
        
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
        
        ttk.Button(add_frame, text="Add Person", 
                  command=self.add_person).pack(fill="x", padx=5, pady=5)
        
        # Get/Delete Person Frame
        action_frame = ttk.LabelFrame(db_frame, text="Get/Delete Person")
        action_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(action_frame, text="Person ID:").pack(anchor="w", padx=5)
        self.id_entry = ttk.Entry(action_frame)
        self.id_entry.pack(fill="x", padx=5)
        
        button_frame = ttk.Frame(action_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Get Person", 
                  command=self.get_person).pack(side="left", expand=True, padx=2)
        ttk.Button(button_frame, text="Delete Person", 
                  command=self.delete_person).pack(side="left", expand=True, padx=2)

    def initialize_agent(self):
        """Initialize the Letta client with custom memory"""
        try:
            self.display_message("System", "Starting agent initialization...")
            
            # Create Letta client
            self.client = create_client()
            self.display_message("System", "Letta client created!")
            
            # trying to get the existing agent
            self.agent_state = self.client.get_agent_by_name("db_agent")
            if self.agent_state:
                self.display_message("System", "Agent already exists!")
                return
            
            # Configure LLM
            tool_llm = LLMConfig(
                model="llama3-groq-8b-8192-tool-use-preview",
                model_endpoint_type='groq',
                model_endpoint='https://api.groq.com/openai/v1',
                model_wrapper=None,
                context_window=8192,
                put_inner_thoughts_in_kwargs=True
            )
            
            # Configure embeddings
            hf_embed = EmbeddingConfig(
                embedding_model="letta-free",
                embedding_endpoint_type="hugging-face",
                embedding_dim=1024,
                embedding_chunk_size=300,
                embedding_endpoint="https://embeddings.memgpt.ai"
            )
            self.display_message("System", "AI parts ready!")
            # Simple memory initialization
            memory = GrpcMemory(
                human="user",
                persona="assistant"
            )
            self.display_message("System", "Configurations ready!")
            
            # Create the agent
            self.agent_state = self.client.create_agent(
                name="db_agent",
                system="I am a database administrator assistant.",  # Simple system prompt for testing
                memory=memory,
                embedding_config=hf_embed,
                llm_config=tool_llm
            )
            
            self.display_message("System", "Database Agent initialized successfully!")
            
        except Exception as e:
            self.display_message("System Error", f"Failed to initialize agent: {str(e)}")
            if hasattr(e, '__cause__'):
                self.display_message("System Error", f"Caused by: {str(e.__cause__)}")

    def send_message(self, message=None):
        """Send a message to the agent"""
        if message is None:
            message = self.message_input.get()
            
        if message.strip():
            # Display user message
            self.display_message("User", message)
            self.message_input.delete(0, tk.END)
            
            # Process agent response in a separate thread
            thread = threading.Thread(target=self.process_agent_response, args=(message,))
            thread.start()
            
    def process_agent_response(self, message):
        """Process the agent's response in a separate thread"""
        try:
            response = self.client.send_message(
                agent_id=self.agent_state.id,
                role="user",
                message=message
            )
            
            self.root.after(0, self.display_message, "Agent", response)
            
        except Exception as e:
            self.root.after(0, self.display_message, "System Error", 
                          f"Error getting response: {str(e)}")

    def display_message(self, sender, message):
        """Display a message in the chat window"""
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"\n{sender}: {message}\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def add_person(self):
        """Add a person using the form data"""
        name = self.name_entry.get()
        age = self.age_entry.get()
        location = self.location_entry.get()
        
        if not all([name, age, location]):
            self.display_message("System", "Please fill all fields")
            return
            
        try:
            age = int(age)
        except ValueError:
            self.display_message("System", "Age must be a number")
            return
            
        message = f"Add a new person named {name}, age {age}, from {location}"
        self.send_message(message)
        
        # Clear form
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)

    def get_person(self):
        """Get person details by ID"""
        person_id = self.id_entry.get()
        if not person_id:
            self.display_message("System", "Please enter a person ID")
            return
            
        try:
            person_id = int(person_id)
        except ValueError:
            self.display_message("System", "ID must be a number")
            return
            
        self.send_message(f"Get details for person with ID {person_id}")

    def delete_person(self):
        """Delete person by ID"""
        person_id = self.id_entry.get()
        if not person_id:
            self.display_message("System", "Please enter a person ID")
            return
            
        try:
            person_id = int(person_id)
        except ValueError:
            self.display_message("System", "ID must be a number")
            return
            
        self.send_message(f"Delete person with ID {person_id}")

def main():
    root = tk.Tk()
    app = GrpcAgentChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
