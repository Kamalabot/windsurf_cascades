# Code Extraction Procedure

## Overview
This document outlines the process of extracting and formatting Python code blocks from the Medium article titled "Build a Local Reliable RAG Agent Using CrewAI and Groq".

## Tools Used
- Python 3.x
- BeautifulSoup4 for HTML parsing
- Requests library for fetching the webpage
- Black formatter for Python code styling

## Requirements
```
requests>=2.31.0
beautifulsoup4>=4.12.2
black>=23.12.1
```

## Process
1. The script `extract_code.py` performs the following steps:
   - Makes an HTTP request to the Medium article URL
   - Parses the HTML content using BeautifulSoup
   - Identifies all code blocks within `<pre>` tags
   - For each code block:
     * Separates actual code from output/debug messages
     * Formats the code using Black formatter
     * Preserves execution output as docstring examples
   - Combines all formatted code into a single Python file
   - Adds proper documentation and section separators

## Code Processing Features
1. Code Cleaning:
   - Removes common artifacts like "Copy code" text
   - Separates code from output using pattern matching
   - Identifies output markers like '[DEBUG]:', '[INFO]:', 'Thought:', etc.

2. Code Formatting:
   - Applies PEP 8 style guidelines using Black
   - Maintains proper indentation and spacing
   - Handles special cases where formatting isn't possible

3. Output Preservation:
   - Stores execution outputs as docstrings
   - Maintains the relationship between code and its output
   - Provides clear examples of code execution results

## Usage
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the extraction script:
   ```bash
   python extract_code.py
   ```

## Output
The script creates an `extract_data` directory containing a single Python file named `combined_code.py`. This file includes:
- Properly formatted Python code blocks
- Clear separation between different code sections
- Documentation comments and source attribution
- Example outputs preserved as docstrings
- Visual separation using comments and horizontal lines

## Note
Please be mindful of copyright and usage rights when extracting and using code from online sources. Always provide proper attribution and follow the article's licensing terms.
