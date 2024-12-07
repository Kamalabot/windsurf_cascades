import requests
from bs4 import BeautifulSoup
import os
import black
import re

def format_python_code(code):
    try:
        # Remove any leading/trailing whitespace
        code = code.strip()
        
        # Try to format the code using black
        formatted_code = black.format_str(code, mode=black.FileMode())
        return formatted_code
    except Exception as e:
        # If formatting fails, return the original code
        print(f"Warning: Could not format a code block: {str(e)}")
        return code

def clean_code_block(code):
    # Remove common artifacts from code blocks
    code = re.sub(r'Copy code', '', code)
    
    # Split into lines
    lines = code.split('\n')
    
    # Separate code from output
    code_lines = []
    output_lines = []
    current_section = code_lines
    
    for line in lines:
        # Check for common output markers
        if any(marker in line for marker in ['[DEBUG]:', '[INFO]:', '> Entering new', '> Finished chain', 'Thought:', 'Action:', 'Final Answer:']):
            current_section = output_lines
        elif line.strip() and not line.startswith('#'):
            current_section.append(line)
    
    # Combine code lines and format them
    code_block = '\n'.join(code_lines).strip()
    output_block = '\n'.join(output_lines).strip()
    
    return code_block, output_block

def extract_code_blocks(url):
    try:
        # Send a request to the Medium article
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all pre tags containing code
        code_blocks = soup.find_all('pre')
        
        # Create extract_data directory if it doesn't exist
        if not os.path.exists('extract_data'):
            os.makedirs('extract_data')
        
        # Combine all code blocks into a single file
        output_file = 'extract_data/combined_code.py'
        with open(output_file, 'w') as f:
            f.write('"""Combined code from Medium article\n')
            f.write('Source: https://medium.com/the-ai-forum/build-a-local-reliable-rag-agent-using-crewai-and-groq-013e5d557bcd\n"""\n\n')
            
            for i, block in enumerate(code_blocks, 1):
                code = block.get_text()
                if code.strip():
                    # Clean and separate code from output
                    code_block, output_block = clean_code_block(code)
                    
                    if code_block:
                        # Write code block with proper separation
                        f.write(f'# Code Block {i}\n')
                        f.write(f'{"#" * 80}\n')
                        try:
                            formatted_code = format_python_code(code_block)
                            f.write(formatted_code)
                        except Exception:
                            f.write(code_block)
                        f.write('\n\n')
                        
                        # Write output if exists
                        if output_block:
                            f.write('"""\nExample Output:\n')
                            f.write(output_block)
                            f.write('\n"""\n\n')
            
        print(f'Successfully saved all formatted code blocks to {output_file}')
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    url = "https://medium.com/the-ai-forum/build-a-local-reliable-rag-agent-using-crewai-and-groq-013e5d557bcd"
    extract_code_blocks(url)
