import os
import re
from docx import Document
from docx.shared import Pt
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import Table
from docx.text.paragraph import Paragraph

# Author: Oleg Telegin

# Find the font size
def get_first_non_default_font_size(paragraph):
    for run in paragraph.runs:
        if run.font.size:
            return run.font.size.pt
    return "Default"

# Find footnotes
def is_numeric_and_small(run):
    numeric_pattern = re.compile(r"^\d+(\s*|,\s*)?$")
    return numeric_pattern.match(run.text) and run.font.size and run.font.size < Pt(9)

# Write paragraph
def write_paragraph(file, paragraph):
    font_size = get_first_non_default_font_size(paragraph)
    file.write(f"(Font Size: {font_size}) ")
    for run in paragraph.runs:
        if run.font.strike:
            file.write(f"\\strikethrough{{{run.text}}}")
        elif is_numeric_and_small(run):
            file.write(f"^{run.text}")
        else:
            file.write(run.text)
    file.write("\n")

# Write table
def write_table(file, table):
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                write_paragraph(file, paragraph)
        file.write("\n")

# Process 1 file
def extract_content(docx_path, txt_path):
    doc = Document(docx_path)
    with open(txt_path, 'w', encoding='utf-8') as file:
        for child in doc.element.body:
            if isinstance(child, CT_P):
                paragraph = Paragraph(child, doc)
                write_paragraph(file, paragraph)
            elif isinstance(child, CT_Tbl):
                table = Table(child, doc)
                write_table(file, table)

# Process all files in a folder
def process_docx_files_in_folder(input_folder_path, output_folder_path):
    # Ensure the output folder exists
    os.makedirs(output_folder_path, exist_ok=True)

    # Iterate over all .docx files in the input folder
    for filename in os.listdir(input_folder_path):
        # Skip temporary files created by Word
        if filename.endswith('.docx') and not filename.startswith('~$'):
            docx_file_path = os.path.join(input_folder_path, filename)
            output_txt_file = os.path.join(output_folder_path, filename.replace('.docx', '.txt'))
            extract_content(docx_file_path, output_txt_file)
            print(f"Processed {filename}")

# Paths and function call
input_folder_path = '../Data/bluebook_prepare/docx_files'
output_folder_path = '../Data/bluebook_prepare/txt_transcripts'
process_docx_files_in_folder(input_folder_path, output_folder_path)
