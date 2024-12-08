# LaTeX Resume

This is a LaTeX-based resume template with a clean, professional design.

## Prerequisites

To compile this resume, you need a LaTeX distribution and PDF tools installed. On Ubuntu/Debian, you can install them using:

```bash
sudo apt-get update
sudo apt-get install texlive-full
sudo apt-get install texlive-latex-extra
sudo apt-get install texlive-fonts-extra
sudo apt-get install poppler-utils  # For pdftotext utility
```

## Converting PDF to LaTeX

### Conversion Methods

#### Method 1: Text Extraction
1. Extract text while preserving layout:
```bash
pdftotext -layout your_resume.pdf your_resume.txt
```
2. Manually transfer content to LaTeX template

#### Method 2: Image-based Conversion
1. Convert PDF to high-resolution images:
```bash
pdftoppm -png -r 300 input.pdf output_prefix
```
2. Use OCR tools like `pix2tex` or Tesseract to convert images to LaTeX

#### Method 3: Manual Reconstruction
1. Open the original PDF
2. Manually recreate the content in the LaTeX template
3. Ensure formatting and structure match the original document

### Conversion Workflow Block Diagram

```
+-------------------+     +-------------------+     +-------------------+
|   Original PDF    |     |   Text Extraction |     |   LaTeX Template  |
|                   | --> |   (pdftotext)     | --> |   (Manual Edit)   |
|  Kamal_Raj_Resume |     |                   |     |                   |
|      .pdf         |     |   Preserve Layout |     |  Restructure Data |
+-------------------+     +-------------------+     +-------------------+
                                                            |
                                                            v
+-------------------+     +-------------------+     +-------------------+
|   Compiled PDF    | <-- |   LaTeX Compiler  | <-- |   Updated .tex    |
|                   |     |   (pdflatex)      |     |   File            |
|  Final Resume     |     |                   |     |                   |
|      .pdf         |     |   Generate PDF    |     |  Refined Content  |
+-------------------+     +-------------------+     +-------------------+

Workflow Steps:
1. Extract text from original PDF
2. Manually edit and structure in LaTeX template
3. Compile updated LaTeX file to generate new PDF
```

### Detailed Workflow Description
- **Text Extraction**: Use `pdftotext` to preserve layout and extract content
- **Manual Editing**: Restructure content in LaTeX template, improve formatting
- **Compilation**: Use `pdflatex` to generate the final PDF document

### Recommended Tools
- `pdftotext`: Text extraction
- `pdftoppm`: PDF to image conversion
- `pix2tex`: AI-powered image to LaTeX conversion
- Tesseract OCR: Open-source OCR tool

### Troubleshooting
- If automated conversion fails, resort to manual content transfer
- Check for rate limits when using AI-powered conversion tools
- Verify formatting and content accuracy after conversion

### Best Practices
- Preserve original formatting and structure
- Use a consistent LaTeX template
- Proofread and manually adjust content as needed

## Compiling the Resume

To compile the resume into a PDF, run:

```bash
pdflatex Kamal_Raj_Resume.tex
```

This will generate `Kamal_Raj_Resume.pdf` in the same directory.

## Customization

Please update the following information in the `Kamal_Raj_Resume.tex` file:
1. Contact information
2. Overview section
3. Skills and technical expertise
4. Work experience and projects
5. Responsibilities
6. Any additional sections you'd like to add

## Structure

The resume is organized into several sections:
- Contact Information
- Overview
- Skills
- Experience
- Key Projects
- Responsibilities
