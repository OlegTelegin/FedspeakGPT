import os
import re

# Author: Oleg Telegin

# Concatenate consecutive footnote paragraphs (later we move them to the correct place in the text)
def process_paragraphs(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    delimiter_pattern = r'(\(Font Size: [^\)]+\)\s)'
    chunks = re.split(delimiter_pattern, text)
    content_chunks = chunks[::2]  # Extracting the content
    delimiters = chunks[1::2]  # Extracting the delimiters

    processed_chunks = []
    skip_indices = set()  # Use a set to track indices of chunks to skip

    for index, chunk in enumerate(content_chunks):
        if index in skip_indices:
            processed_chunks.append("\n")  # Replace skipped chunk with a newline
            continue

        type_1_match = re.match(r'^\^\d{1,2}([ \t]+|[a-zA-Z]|\n)', chunk)

        if type_1_match:
            # print(chunk)
            while not chunk.strip().endswith('.') and not chunk.strip().endswith('.”') and not chunk.strip().endswith('."') and (index + 1 < len(content_chunks)):
                next_index = index + 1
                next_chunk = content_chunks[next_index]
                chunk = chunk.rstrip('\n') + ' ' + next_chunk
                skip_indices.add(next_index)  # Mark next chunk to be skipped
                index = next_index  # Move to the next chunk for potential further concatenation

        processed_chunks.append(chunk)

    # Combine the processed chunks with their delimiters
    modified_text = ''.join([f"{delimiters[i]}{processed_chunks[i+1]}" for i in range(len(processed_chunks)-1)])

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(modified_text)

# Process all files in a folder
def process_all_files_in_folder(input_folder_path, output_folder_path):
    os.makedirs(output_folder_path, exist_ok=True)  # Ensure the output folder exists

    for filename in os.listdir(input_folder_path):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, filename)
            process_paragraphs(input_file_path, output_file_path)
            print(f"Processed {filename}")

# Paths and function call
input_folder_path = '../Data/bluebook_prepare/no_strikethrough_manual'
output_folder_path = '../Data/bluebook_prepare/concatenate_pars_footnotes'
process_all_files_in_folder(input_folder_path, output_folder_path)
