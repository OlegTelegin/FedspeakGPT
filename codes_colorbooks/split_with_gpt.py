import os
import re
import pandas as pd
import time
import openai
from openai import OpenAI

# Author: Oleg Telegin

# Initialize OpenAI client
client = OpenAI()

# Split into chunks and find specific entries
def get_chunks_with_specific_entries(txt_file_path, specific_entries):
    # Read the .txt file
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into chunks and delimiters
    pattern = re.compile(r'(\{[^}]*first[^}]*\})')
    parts = pattern.split(text)
    chunks = parts[::2]
    delimiters = parts[1::2]
    chunks = chunks[1:]

    matched_chunks = []
    matched_delimiters = []

    # Process each delimiter and check for specific entries
    for index, delimiter in enumerate(delimiters):
        entries = delimiter.strip("{}").split(",")
        entries = [entry.strip() for entry in entries]  # Clean up whitespace around entries
        unique_entries = set(entries)  # Using a set to automatically ensure uniqueness

        matched_entries = [entry for entry in unique_entries if entry in specific_entries]

        # Add the corresponding chunk to the list if criteria are met
        if len(matched_entries) > 1:
            matched_chunks.append((index + 1, matched_entries, chunks[index]))
            matched_delimiters.append(delimiter)
    print(matched_chunks)
    print(matched_delimiters)
    return matched_chunks, matched_delimiters, chunks, delimiters

# Split matched entries into separate letters, remove duplicates.
def process_matched_entries(matched_entries):
    processed_entries = set(''.join(matched_entries))
    return processed_entries

# Send a GPT API request using the openai library.
def send_gpt_request(system_content, user_content):
  response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    # model="gpt-4-1106-preview",
    messages=[{"role": "system", "content": system_content}, {"role": "user", "content": user_content}],
    temperature=0,
    max_tokens=2000,
  )
  time.sleep(10)
  return response

# Process 1 text chunk
def process_chunk(chunk, delimiter, index, processed_entries, output_file):
    for entry in processed_entries:
        # Split the delimiter by commas and remove the curly braces
        parts_dop = delimiter.strip("{}").split(",")
        # Take the first two elements
        first_two_parts = parts_dop[:2]
        # Append the entry
        first_two_parts.append(entry)
        # Join the elements into a new string and enclose with curly braces
        new_delimiter = "{" + ",".join(first_two_parts) + "}"

        entry_main = "Alternative " + entry
        other_entries = processed_entries - {entry}  # Get other entries by removing the current one

        if len(processed_entries) == 1:
            print("Only 1 entry")
        elif len(processed_entries) == 2:
            entry_dop = "Alternative " + other_entries.pop()  # There's only one other entry, so pop() works here
        else:
            # Join the other entries with commas for 3 or more entries
            entry_dop = "Alternatives " + ", ".join(other_entries)

        # print(f"Main entry: {entry_main}, Other entries: {entry_dop}")
        system_content = f"""You're an expert in Natural Language Processing. You can extract information from the text, using the wording of the original text when possible. You're given with the chunk of text, you get all the information about {entry_main} out of it, ignoring information about {entry_dop}. Use the wording from the text as much as possible, try not to change the meaning of what is written about {entry_main}. If a text uses generalization, that is, it discusses all Alternatives without naming them individually (for instance, discussing 'each of the Alternatives', 'every Alternative', or something similar), then it also applies to {entry_main}. In this case, you can change the wording using '{entry_main}' as the action object, but wording can only be changed in replacing the generalized Alternatives indication with {entry_main}. If there is no information about {entry_main} in the text - return 'No information about {entry_main} in the text.'"""
        user_content = chunk
        # print(system_content)
        response = send_gpt_request(system_content, user_content)
        print(f"Response for chunk {index}, entry '{entry}':", response.choices[0].message.content)
        tag_string = new_delimiter + " " + response.choices[0].message.content + "\n"
        output_file.write(tag_string)

# Process 1 file
def main_processing(txt_file_path, output_file_path, specific_entries):
    matched_chunks, matched_delimiters, chunks, delimiters = get_chunks_with_specific_entries(txt_file_path, specific_entries)
    # Open the output file once and use it throughout
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for index, (chunk, delimiter) in enumerate(zip(chunks, delimiters), start=1):
            # Check if the chunk is in matched_chunks
            is_matched = False
            for matched_index, matched_entries, matched_chunk_text in matched_chunks:
                if chunk == matched_chunk_text:
                    is_matched = True
                    processed_entries = process_matched_entries(matched_entries)
                    # Call the processing function for this matched chunk
                    process_chunk(chunk, delimiter, matched_index, processed_entries, output_file)
                    break  # Each chunk can only match once, break after finding a match

            # If the chunk wasn't matched, write it directly
            if not is_matched:
                output_file.write(f"{delimiter}{chunk}")

# Process all files in a folder
def process_all_files(input_folder, output_folder, specific_entries):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            txt_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            print(f"Processing {filename}...")
            main_processing(txt_file_path, output_file_path, specific_entries)

# Paths and function call
specific_entries = ['A', 'B', 'C', 'D', 'ABCD', 'ABC', 'ABD', 'ACD', 'BCD', 'AB', 'AC', 'BC', 'AD', 'BD', 'CD']
input_folder = '../Data/bluebook_prepare/split_sentences'
output_folder = '../Data/bluebook_prepare/split_with_gpt'

process_all_files(input_folder, output_folder, specific_entries)
