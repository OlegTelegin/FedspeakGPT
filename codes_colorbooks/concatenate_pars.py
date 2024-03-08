import os
import re
from collections import Counter

# Author: Oleg Telegin

# Append text chunks if doesn't end with .
def append_chunks_and_select_delimiter(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    delimiter_pattern = r'(\(Font Size: [^\)]+\)\s)'
    chunks = re.split(delimiter_pattern, text)

    content_chunks = chunks[0::2]
    delimiters = chunks[1::2]
    content_chunks = content_chunks[1:]

    appended_chunks = []
    appended_delimiters = []
    temp_chunk = ""
    temp_delimiters = []

    for i in range(len(content_chunks)):
        current_chunk = content_chunks[i].strip()
        current_delimiter = delimiters[i]

        # Append the current chunk to the temp_chunk if it doesn't end properly or if it's the last chunk
        if not current_chunk.endswith(('.', '."', '.”')):
            temp_delimiters.append(current_delimiter)
            if i == len(content_chunks) - 1:
                # Count the frequencies
                delimiter_counts = Counter(temp_delimiters)
                # Get the two most common elements and their counts
                two_most_common = delimiter_counts.most_common(2)
                # Check if there's a tie and if there are at least two elements
                if len(two_most_common) > 1 and two_most_common[0][1] == two_most_common[1][1]:
                    # There's a tie, select the second entry
                    most_common_delimiter = two_most_common[1][0]  # Selects the second entry in case of a tie
                else:
                    # No tie or not enough elements for a tie, select the first entry
                    most_common_delimiter = two_most_common[0][0]
                appended_chunks.append(current_chunk)
                appended_delimiters.append(most_common_delimiter)
            else:
                # Append the accumulated temp_chunk and its most frequent delimiter
                content_chunks[i + 1] = current_chunk.strip() + ' ' + content_chunks[i + 1]
        else:
            # If the current chunk ends properly and is not being accumulated, append it directly
            appended_chunks.append(current_chunk)
            # Find the most frequent delimiter among temp_delimiters
            temp_delimiters.append(current_delimiter)
            # Count the frequencies
            delimiter_counts = Counter(temp_delimiters)
            # Get the two most common elements and their counts
            two_most_common = delimiter_counts.most_common(2)
            # Check if there's a tie and if there are at least two elements
            if len(two_most_common) > 1 and two_most_common[0][1] == two_most_common[1][1]:
                # There's a tie, select the second entry
                most_common_delimiter = two_most_common[1][0]  # Selects the second entry in case of a tie
            else:
                # No tie or not enough elements for a tie, select the first entry
                most_common_delimiter = two_most_common[0][0]
            appended_delimiters.append(most_common_delimiter)
            # Reset temp variables for the next accumulation
            temp_delimiters = []

    # Combine the processed chunks with their corresponding delimiters
    modified_text = ''.join([f"\n{delim}{chunk}" for delim, chunk in zip(appended_delimiters, appended_chunks)])

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(modified_text)

# Process all files in a folder
def process_folder(input_folder_path, output_folder_path):
    # Ensure the output folder exists
    os.makedirs(output_folder_path, exist_ok=True)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, filename)

            append_chunks_and_select_delimiter(input_file_path, output_file_path)
            print(f"Processed {filename}")

# Paths and function call
input_folder_path = '../Data/bluebook_prepare/change_titles'
output_folder_path = '../Data/bluebook_prepare/append_pars'
process_folder(input_folder_path, output_folder_path)
