import os
import re

# Author: Oleg Telegin

# Delete strikethrough text
def modify_text(input_file_path, output_file_path):
    # Read the content of the file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace ^digit^digit with ^digitdigit using regex
    modified_content = re.sub(r'\^(\d+)\^(\d+)', r'^\1\2', content)

    # Delete all \strikethrough{} tags and their contents
    modified_content = re.sub(r'\\strikethrough\{[^}]*\}', '', modified_content)

    # Write the modified content to a new file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)

# Process all files in a folder
def process_folder(input_folder_path, output_folder_path):
    # Ensure the output folder exists
    os.makedirs(output_folder_path, exist_ok=True)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder_path):
        # Process only .txt files
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, filename)
            modify_text(input_file_path, output_file_path)
            print(f"Processed {filename}")

# Paths and function call
input_folder_path = '../Data/bluebook_prepare/txt_transcripts'
output_folder_path = '../Data/bluebook_prepare/no_strikethrough'
process_folder(input_folder_path, output_folder_path)
