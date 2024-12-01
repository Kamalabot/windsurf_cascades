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

If you have an existing PDF resume that you want to convert to LaTeX:

1. Convert PDF to text while preserving layout:
```bash
pdftotext -layout your_resume.pdf your_resume.txt
```

2. Use the text content to update the LaTeX template in `Kamal_Raj_Resume.tex`

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
