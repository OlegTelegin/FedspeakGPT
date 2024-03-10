import os
import re
import pandas as pd
import time
import openai
from openai import OpenAI

# Author: Oleg Telegin

# Initialize OpenAI client
client = OpenAI()

# Get chunks and Alternatives
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
        if len(matched_entries) > 0:
            matched_chunks.append((index + 1, matched_entries, chunks[index]))
            matched_delimiters.append(delimiter)
    # print(matched_chunks)
    # print(matched_delimiters)
    return matched_chunks, matched_delimiters, chunks, delimiters

# Send a GPT API request using the openai library
def send_gpt_request(system_content, user_content):
  response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    # model="gpt-4-1106-preview",
    messages=[{"role": "system", "content": system_content}, {"role": "user", "content": user_content}],
    temperature=0,
    max_tokens=3000,
  )
  time.sleep(5)
  return response

# Process 1 text chunk
def process_chunk(matched_chunks, matched_delimiters, output_file, entries_dict):
    sentence_pattern = re.compile(r'(?<=\.)\s|(?<=\."\s)|(?<=\.”)\s')
    for index, matched_entries, chunk_text in matched_chunks:
        sentences = sentence_pattern.split(chunk_text)
        sentences = [sentence for sentence in sentences if sentence.strip()]
        print(index)
        new_delimiter = "{" + "mention" + matched_entries[0] + "}"
        # print(new_delimiter)

        entry_main = entries_dict.get(matched_entries[0], "Default Value")
        # print(entry_main)
        system_content = f"""You're an expert in Natural Language Processing. You can extract information from the text, using the 
wording of the original text when possible."""

        user_content = f"""I will give you instructions and text about {entry_main}. Instructions: the first sentence of 
the text discusses {entry_main}. It may discuss {entry_main} explicitly or using generalization (for instance, 
discussing 'each of the Alternatives', 'every Alternative', or something similar). I need to figure out what part of 
the following text also discusses {entry_main}, possible market reaction to it, the Committee's thoughts about it, 
staff's thoughts about it, assumptions under {entry_main}, language used in {entry_main}, current economic stance 
leading to pick {entry_main}, or the consequences of choosing {entry_main}. It could be the whole text or part of the 
text up to some point. You're given with the chunk of text, rewrite it as long as it relates to {entry_main} in any of 
the ways described earlier. Stop when the topic has changed to something unrelated in any way to {entry_main}. Don't 
change any wording while rewriting the text. Text: {chunk_text}"""
        # print(system_content)
        # print(user_content)
        # Check if chunk_text is more than 1 sentence length
        if len(sentences) > 1:
            # More than one sentence, proceed with sending a GPT request
            response = send_gpt_request(system_content, user_content)
            # Assuming the response structure is as before, adjust as necessary
            response_text = response.choices[0].message.content
            tag_string = new_delimiter + " " + response_text + "\n"
        else:
            # Only one sentence, use chunk_text directly
            response_text = chunk_text
            tag_string = new_delimiter + response_text
        # print(f"Response for chunk {index} of Alternative {matched_entries[0]}:", response.choices[0].message.content)
        output_file.write(tag_string)

# Process all files in a folder
def main_processing(folder_path, output_folder, specific_entries, entries_dict):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            txt_file_path = os.path.join(folder_path, filename)
            output_file_path = os.path.join(output_folder, filename)
            print(f"Processing {filename}...")
            matched_chunks, matched_delimiters, chunks, delimiters = get_chunks_with_specific_entries(txt_file_path,
                                                                                                      specific_entries)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                process_chunk(matched_chunks, matched_delimiters, output_file, entries_dict)

specific_entries = ['A', 'B', 'C', 'D', 'ABCD', 'ABC', 'ABD', 'ACD', 'BCD', 'AB', 'AC', 'BC', 'AD', 'BD', 'CD']
specific_entries_values = ['Alternative A', 'Alternative B', 'Alternative C', 'Alternative D', 'four Alternatives (Alternatives A, B, C, and D)', 'three Alternatives (Alternatives A, B, and C)', 'three Alternatives (Alternatives A, B, and D)', 'three Alternatives (Alternatives A, C, and D)', 'three Alternatives (Alternatives B, C, and D)', 'two Alternatives (Alternatives A and B)', 'two Alternatives (Alternatives A and C)', 'two Alternatives (Alternatives B and C)', 'two Alternatives (Alternatives A and D)', 'two Alternatives (Alternatives B and D)', 'two Alternatives (Alternatives C and D)']
entries_dict = dict(zip(specific_entries, specific_entries_values))
folder_path = '../Data/bluebook_prepare/append_mentions_manual/test'
output_folder = '../Data/bluebook_prepare/cut_mentions'

main_processing(folder_path, output_folder, specific_entries, entries_dict)
