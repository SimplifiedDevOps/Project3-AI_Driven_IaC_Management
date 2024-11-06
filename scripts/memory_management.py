# scripts/memory_management.py
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
import openai

# Initialize LangChain and Memory
def initialize_langchain_with_memory():
    memory = ConversationBufferMemory()
    llm = OpenAI(api_key="your_openai_api_key")
    return llm, memory

# Store past interactions in memory
def store_interaction(memory, prompt, response):
    memory.save_context({"prompt": prompt}, {"response": response})

# Generate response with memory context
def generate_response_with_memory(prompt, llm, memory):
    # Retrieve memory context
    context = memory.load_memory_variables({}).get("history", "")
    # Generate response with context included
    full_prompt = f"{context}\n\n{prompt}"
    response = llm(full_prompt)
    # Store the new prompt-response pair
    store_interaction(memory, prompt, response)
    return response

if __name__ == "__main__":
    # Initialize LangChain and memory
    llm, memory = initialize_langchain_with_memory()

    # Example session with multiple prompts
    prompts = [
        "Create a Terraform template for an EC2 instance.",
        "Add a security group to allow SSH access."
    ]
    
    for prompt in prompts:
        response = generate_response_with_memory(prompt, llm, memory)
        print("Response:", response)
