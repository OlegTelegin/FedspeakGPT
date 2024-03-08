import os
import re

# Author: Oleg Telegin

# Add a draft
def find_and_combine_files_for_folder(folder_a, source_folder, output_folder):
    pattern_a = re.compile(r'(\d{4})(\d{2})_([ABCD])\.txt')

    for file_a_name in os.listdir(folder_a):
        match = pattern_a.match(file_a_name)
        if match:
            # Extract year, month from file_a_name
            year, month, letter = match.groups()
            # Construct a regex pattern for searching corresponding files
            pattern = f"{year}{month}s_{letter}.*\\.txt"
            compiled_pattern = re.compile(pattern)

            combined_content = []

            # Search for matching files in the source folder
            for filename in os.listdir(source_folder):
                if compiled_pattern.match(filename):
                    with open(os.path.join(source_folder, filename), 'r', encoding='utf-8') as file:
                        content = file.read().rstrip()  # Read and remove trailing empty lines
                        combined_content.append(content)

            # Append content from file_a after collecting from matched files
            file_a_path = os.path.join(folder_a, file_a_name)
            with open(file_a_path, 'r', encoding='utf-8') as file_a:
                combined_content.append(file_a.read().rstrip())  # Also remove trailing empty lines from file_a

            # Define output file path based on file_a_name
            output_file_name = f"{year}{month}_{letter}.txt"
            output_file_path = os.path.join(output_folder, output_file_name)

            # Write combined content to the output file
            with open(output_file_path, 'w', encoding='utf-8') as output:
                output.write("\n".join(combined_content))

            print(f"Combined file created: {output_file_path}")

# Paths and function call
folder_a = '../Data/bluebook_prepare/store_alternatives'
source_folder = '../Data/alternatives_drafts'
output_folder = '../Data/bluebook_prepare/final_alternatives'
find_and_combine_files_for_folder(folder_a, source_folder, output_folder)
