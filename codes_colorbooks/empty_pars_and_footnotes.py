import os
import re

# Author: Oleg Telegin

# Drop footnote symbols and empty paragraphs
def process_chunks(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    delimiter_pattern = r'(\(Font Size: [^\)]+\)\s)'
    chunks = re.split(delimiter_pattern, text)
    content_chunks = chunks[::2]  # Extracting the content
    delimiters = chunks[1::2]  # Extracting the delimiters
    content_chunks = content_chunks[1:]
    # Define a pattern to match "^number^number"
    # pattern_to_remove = re.compile(r'\^\d+\^\d+')
    pattern_to_remove = re.compile(r'\^\d+')
    # Filter out empty content chunks and their corresponding delimiters
    non_empty_content_chunks = []
    non_empty_delimiters = []
    for content, delimiter in zip(content_chunks, delimiters):
        # Remove the specified pattern from content
        modified_content = re.sub(pattern_to_remove, '', content)

        if modified_content.strip() != '':  # Check if the chunk is not just a newline after modification
            non_empty_content_chunks.append(modified_content)
            non_empty_delimiters.append(delimiter)

    # Recombine the chunks with their corresponding delimiters
    final_text = ''.join([f"{delim}{content}" for delim, content in zip(non_empty_delimiters, non_empty_content_chunks)])

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(final_text)

# Process all files in a folder
def process_files_in_folder(input_folder_path, output_folder_path):
    # Ensure the output folder exists
    os.makedirs(output_folder_path, exist_ok=True)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, filename)
            process_chunks(input_file_path, output_file_path)
            print(f"Processed {filename}")

# Paths and function call
input_folder_path = '../Data/bluebook_prepare/move_footnotes'
output_folder_path = '../Data/bluebook_prepare/empty_pars_and_footnotes'
process_files_in_folder(input_folder_path, output_folder_path)
