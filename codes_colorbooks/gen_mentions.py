import os
import re
import pandas as pd

# author: Oleg Telegin

# Function to split the text into chunks and delimiters
def split_into_chunks_and_delimiters(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Regular expression to match delimiters and capture text in between
    pattern = re.compile(r'(\{[^}]*first[^}]*\})')

    # Split the text and capture delimiters
    parts = pattern.split(text)
    chunks = parts[::2]  # Even indices are chunks
    delimiters = parts[1::2]  # Odd indices are delimiters
    chunks = chunks[1:]  # 1st chunk is empty

    return chunks, delimiters

# Function to get the mapping from the numbered mentions to Alternatives A, B, C, D,
# Or their combinations (distinguishing between those pointing to an Alternative and those comparing to it)
# Also gets exclusions list - which mentions we should exclude
def read_matching_table(xlsx_file_path):
    df = pd.read_excel(xlsx_file_path, sheet_name=0)  # The table is in the first sheet
    matching_table = {}
    exclusions_table = {}
    for _, row in df.iterrows():
        entry = str(row.iloc[1])  # The entries are in the second column
        exclusions = [str(int(float(ex))) for ex in str(row.iloc[2]).split(",")] if pd.notna(row.iloc[2]) else []
        options = row[3:33]
        matched_option = options.idxmax()  # Find the column name with the '1'
        matching_table[entry] = matched_option  # Map entry to its option
        exclusions_table[entry] = exclusions  # Store exclusions
    return matching_table, exclusions_table

# Construct new delimiters
def update_delimiters(delimiters, matching_table, exclusions_table):
    new_delimiters = []
    for delimiter in delimiters:
        # Splitting the entries inside the delimiter
        entries = delimiter.strip("{}").split(",")
        updated_entries = []
        for entry in entries:
            entry = entry.strip()
            # Exclude entries based on exclusions table
            if entry in exclusions_table:
                excluded_entries = exclusions_table[entry]
                entries = [e for e in entries if e not in excluded_entries]
        for entry in entries:
            if entry in matching_table:
                # If the entry is found in the matching table, replace it with the corresponding option
                updated_entries.append(matching_table[entry])
                # print(matching_table[entry])
            else:
                # If not found, keep the entry as is
                updated_entries.append(entry)
        # Constructing new delimiter with updated entries
        # print(updated_entries)
        new_delimiter = "{" + ",".join(updated_entries) + "}"
        new_delimiters.append(new_delimiter)
    return new_delimiters

# Process 1 file in the folder
def process_txt_file(txt_file_path, xlsx_file_path_a, xlsx_file_path_b, output_file_path):
    chunks, delimiters = split_into_chunks_and_delimiters(txt_file_path)
    if delimiters and "{four" in delimiters[0]:
        xlsx_file_path = xlsx_file_path_b
    else:
        xlsx_file_path = xlsx_file_path_a
    matching_table, exclusions_table = read_matching_table(xlsx_file_path)
    new_delimiters = update_delimiters(delimiters, matching_table, exclusions_table)

    # Combine chunks with new delimiters and write to a new .txt file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for chunk, new_delimiter in zip(chunks, new_delimiters):
            output_file.write(new_delimiter + chunk)
        # Add the last chunk if the number of chunks is greater than new delimiters
        if len(chunks) > len(new_delimiters):
            output_file.write(chunks[-1])

# Process all files in the folder
def process_folder(input_folder, output_folder, xlsx_file_path_a, xlsx_file_path_b):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            txt_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            process_txt_file(txt_file_path, xlsx_file_path_a, xlsx_file_path_b, output_file_path)
            print(f"Processed {filename}")

# Paths and function call
input_folder = '../Data/bluebook_prepare/work_with_as_in'
output_folder = '../Data/bluebook_prepare/gen_mentions'
xlsx_file_path_a = '../Data/bluebook_prepare/Phrases3.xlsx'
xlsx_file_path_b = '../Data/bluebook_prepare/Phrases4.xlsx'
process_folder(input_folder, output_folder, xlsx_file_path_a, xlsx_file_path_b)
