import os
import re

# Author: Oleg Telegin

# Store different Alternatives in different files
def process_text_and_store_by_mention(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            with open(input_file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            # Extract year, month, and day from filename
            date_parts = filename.split('_')[0]  # Filename format is "YYYY-MM-DD_other"
            yearmonth = date_parts.replace('-', '')[:6]  # Extract YYYYMM

            # Define the pattern to split text into chunks and delimiters
            pattern = re.compile(r'(\{mention[^}]*\})')
            parts_dop = pattern.split(text)
            chunks_dop = parts_dop[::2]
            chunks_dop = chunks_dop[1:]
            delimiters_dop = parts_dop[1::2]

            new_text_parts = []

            # Iterate through delimiters and chunks
            for delimiter_dop, chunk_dop in zip(delimiters_dop, chunks_dop):
                mention_text = delimiter_dop.strip("{}").replace("mention", "")
                if len(mention_text) > 1:
                    # More than one letter in the mention, split and duplicate
                    for letter in mention_text:
                        new_delimiter = f"{{mention{letter}}}"
                        new_text_parts.append(new_delimiter)
                        new_text_parts.append(chunk_dop)  # Duplicate the chunk for each new delimiter
                else:
                    # Single letter mentions or no mention at all, keep as is
                    new_text_parts.append(delimiter_dop)
                    new_text_parts.append(chunk_dop)

            # Combine the text parts back together
            combined_text = ''.join(new_text_parts)

            parts = pattern.split(combined_text)
            chunks = parts[::2]
            chunks = chunks[1:]
            delimiters = parts[1::2]

            # Prepare a dictionary to store chunks by mention
            mention_chunks = {}

            # Iterate through delimiters and chunks
            for delimiter, chunk in zip(delimiters, chunks):
                mention_text = delimiter.strip("{}").replace("mention", "")
                if mention_text:  # Non-empty mention
                    # Initialize the list in the dictionary if not already present
                    if mention_text not in mention_chunks:
                        mention_chunks[mention_text] = []
                    mention_chunks[mention_text].append(chunk)

            # Write the stored chunks to separate files based on mention
            for mention, chunks in mention_chunks.items():
                output_file_name = f"{yearmonth}_{mention}.txt"
                output_file_path = os.path.join(output_folder, output_file_name)
                if output_file_name != "200904_C.txt":
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(''.join(chunks))
                    print(f"Stored chunks for {mention} in {output_file_name}")

# Paths and function call
input_folder = '../Data/bluebook_prepare/cut_mentions'
output_folder = '../Data/bluebook_prepare/store_alternatives'
process_text_and_store_by_mention(input_folder, output_folder)
