import os
import re

# Author: Oleg Telegin

# Concatenate the text before the next Alternative mention
def process_text_file(input_file_path, output_file_path, specific_entries):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into chunks and delimiters
    pattern = re.compile(r'(\{[^}]*first[^}]*\})')
    parts = pattern.split(text)
    chunks = parts[::2]
    chunks = chunks[1:]
    delimiters = parts[1::2]

    # Prepare pattern to match "No information about Alternative ? in the text."
    info_pattern = re.compile(r'No information about Alternative [ABCD] in the text\.')

    # Indices of chunks to be removed
    indices_to_remove = []

    # Iterate through chunks to find matches
    for i, chunk in enumerate(chunks):
        if info_pattern.search(chunk):
            indices_to_remove.append(i)

    # Remove the identified chunks and their corresponding delimiters
    # Starting from the end to not mess up the indices
    for i in sorted(indices_to_remove, reverse=True):
        del chunks[i]
        del delimiters[i]

    pattern = r'\b(' + '|'.join(map(re.escape, specific_entries)) + r')\b'

    # Reverse iterate through chunks and delimiters
    for i in range(len(chunks) - 1, 0, -1):
        # Check if the current delimiter does not contain any of the specific entries
        if not re.search(pattern, delimiters[i]):
            # Append the current chunk to the previous chunk
            chunks[i-1] = chunks[i-1].rstrip() + " " + chunks[i].lstrip()
            # Remove the current chunk and its delimiter
            del chunks[i]
            del delimiters[i]

    # Combine the remaining chunks with their corresponding delimiters
    combined_text = ''.join([delimiters[i] + chunks[i] for i in range(len(chunks))])

    # Write the combined text to a new file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(combined_text)

# Process all files in a folder
def process_folder(input_folder, output_folder, specific_entries):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            # Process each text file
            process_text_file(input_file_path, output_file_path, specific_entries)
            print(f"Processed {filename}")

# Paths and function call
input_folder = '../Data/bluebook_prepare/split_with_gpt'
output_folder = '../Data/bluebook_prepare/append_mentions'
specific_entries = ['A', 'B', 'C', 'D', 'ABCD', 'ABC', 'ABD', 'ACD', 'BCD', 'AB', 'AC', 'BC', 'AD', 'BD', 'CD']
process_folder(input_folder, output_folder, specific_entries)
