import os
import re
import pandas as pd

# Author: Oleg Telegin

# Create a regex pattern that matches the phrase with any amount of whitespace (including none)
# between each character of the phrase.
def create_flexible_regex(phrase):
    return r'\s*'.join(re.escape(char) for char in phrase) + r'\s*'

# Get the number of Alternatives
def check_for_specific_phrases(content_dop, phrases_list):
    condition1_met = False
    condition2_met = False
    for phrase in phrases_list:
        # Create a flexible regex for the phrase to ignore spaces and newlines
        flexible_regex = create_flexible_regex(phrase)
        if re.search(flexible_regex, content_dop, re.IGNORECASE | re.DOTALL):
            condition1_met = True
    dop_phrase = "Alternative D"
    dop_regex = create_flexible_regex(dop_phrase)
    if re.search(dop_regex, content_dop, re.DOTALL):
        condition2_met = True

    # Both conditions must be met to return "four"
    if condition1_met and condition2_met:
        return "four"
    else:
        return "three"

# Get specific entries
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

    # Process each delimiter and check for specific entries
    for index, delimiter in enumerate(delimiters):
        entries = delimiter.strip("{}").split(",")
        entries = [entry.strip() for entry in entries]  # Clean up whitespace around entries
        # print(entries)
        unique_entries = set(entries)  # Using a set to automatically ensure uniqueness

        matched_entries = [entry for entry in unique_entries if entry in specific_entries]

        # Add the corresponding chunk to the list if criteria are met
        if len(matched_entries) > 1:
            matched_chunks.append((index + 1, matched_entries, chunks[index]))
    # print(matched_chunks)
    return matched_chunks, chunks, delimiters

# Read the list of phrases from an Excel file.
def read_phrases_from_xlsx(xlsx_file_path):
    df = pd.read_excel(xlsx_file_path)
    phrases = df[df.columns[0]].dropna().tolist()[:-4]
    exclusions_table = {}
    direct_mentions = {}
    for _, row in df.iterrows():
        entry = str(row.iloc[1])
        exclusions = [str(int(float(ex))) for ex in str(row.iloc[2]).split(",")] if pd.notna(row.iloc[2]) else []  # Split exclusions into list
        exclusions_table[entry] = exclusions  # Store exclusions
        direct_mentions_dop = row.iloc[3:10].sum()
        direct_mentions[entry]=direct_mentions_dop
    return phrases, exclusions_table, direct_mentions

# Split the text with delimiters and check for phrases.
def split_and_check_phrases(text, phrases, delimiters_for_sentence, exclusions_table, direct_mentions):
    new_delimiters = []
    additional_pattern_and = r'and(?=\s+Alternative)'
    additional_pattern_or = r'or(?=\s+Alternative)'
    additional_pattern_with = r'with(?=\s+Alternative)'
    additional_pattern_and2 = r'AND(?=\s+ALTERNATIVE)'
    additional_pattern_or2 = r'OR(?=\s+ALTERNATIVE)'
    regex_pattern = '|'.join(map(re.escape, delimiters_for_sentence)) + '|' + additional_pattern_and + '|' + additional_pattern_or + '|' + additional_pattern_and2 + '|' + additional_pattern_or2 + '|' + additional_pattern_with
    parts = re.split(regex_pattern, text)
    # Initialize a list to store matched phrases' indices for each part
    matched_phrases_indices = []

    # Iterate over each part of the split text
    for part in parts:
        # Normalize the part by removing spaces and newlines for comparison
        normalized_part = re.sub(r'[\s\n]+', '', part)

        # Initialize a list to store indices of phrases matched in this part
        part_matched_indices = []

        # Iterate over each phrase and its index
        for index, phrase in enumerate(phrases):
            # Normalize the phrase for comparison
            normalized_phrase = re.sub(r'[\s\n]+', '', phrase)

            # Check if the normalized phrase is in the normalized part
            if normalized_phrase in normalized_part:
                # If matched, add the index of the phrase to the list
                part_matched_indices.append(index + 1)  # Using index+1 to match human-readable numbering

        # Add the list of matched indices for this part to the overall list
        matched_phrases_indices.append(part_matched_indices)

    filtered_new_delimiters = []
    for matched_phrases_index in matched_phrases_indices:
        # print(matched_phrases_index)
        # Splitting the entries inside the delimiter
        single_indices = [str(index) for index in matched_phrases_index]
        updated_single_indices = []
        for single_index in single_indices:
            # Exclude entries based on exclusions table
            if single_index in exclusions_table:
                excluded_entries = exclusions_table[single_index]
                # print("a")
                # print(excluded_entries)
                single_indices = [e for e in single_indices if e not in excluded_entries]

        filtered_indices = [index for index in single_indices if direct_mentions.get(index, 0) == 1]
        filtered_new_delimiters.append(filtered_indices)
        for single_index in single_indices:
            updated_single_indices.append(single_index)
        # Constructing new delimiter with updated entries
        # print(updated_entries)
        new_delimiters.append(updated_single_indices)
    # print(filtered_new_delimiters)

    # for part, matched_phrases_index in zip(parts, matched_phrases_indices):
        # print(f"Part: {part}, Indices: {matched_phrases_index}")
    # Return the list of matched phrases' indices for each part
    return filtered_new_delimiters

# Process chunks of the .txt file and print ones with more than one specific entry.
def process_chunks(txt_file_path, output_file_path, phrases, delimiters_for_sentence, exclusions_table, direct_mentions, specific_entries):
    # Capture the returned matched_chunks from get_chunks_with_specific_entries
    matched_chunks, chunks, delimiters = get_chunks_with_specific_entries(txt_file_path, specific_entries)
    all_filtered_new_delimiters = []
    all_filtered_new_chunks = []
    for index, matched_entries, chunk_text in matched_chunks:
        filtered_new_delimiters = split_and_check_phrases(chunk_text, phrases, delimiters_for_sentence, exclusions_table, direct_mentions)
        if all(len(sublist) <= 1 for sublist in filtered_new_delimiters):
            pass
        else:
            print(f"Excluded chunk at index {index} due to multiple entries in a delimiter.")
            all_filtered_new_delimiters.append(filtered_new_delimiters)
            all_filtered_new_chunks.append(chunk_text)
    print("All filtered new delimiters across all chunks:")
    print(all_filtered_new_delimiters)
    print(all_filtered_new_chunks)
    # Write to output file, excluding filtered chunks and their corresponding delimiters
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for chunk, delimiter in zip(chunks, delimiters):
            if chunk not in all_filtered_new_chunks:
                # Write only if the chunk is not in the filtered list
                output_file.write(delimiter + chunk)

# Process all files in a folder
def process_folder(folder_path, xlsx_file_path_a, xlsx_file_path_b, delimiters_for_sentence, specific_entries, specific_phrases):
    os.makedirs(output_folder_path, exist_ok=True)
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            txt_file_path = os.path.join(folder_path, filename)

            with open(txt_file_path, 'r', encoding='utf-8') as file_dop:
                content_dop = file_dop.read()
            alternatives_indicator_dop = check_for_specific_phrases(content_dop, specific_phrases)
            xlsx_file_path = xlsx_file_path_a if alternatives_indicator_dop == "four" else xlsx_file_path_b

            phrases, exclusions_table, direct_mentions = read_phrases_from_xlsx(xlsx_file_path)
            output_file_path = os.path.join(output_folder_path, filename)
            print(f"Processing {filename}...")
            process_chunks(txt_file_path, output_file_path, phrases, delimiters_for_sentence, exclusions_table, direct_mentions, specific_entries)

# Paths, lists, and function call
folder_path = '../Data/bluebook_prepare/gen_mentions'
output_folder_path = '../Data/bluebook_prepare/split_sentences'
xlsx_file_path_a = '../Data/bluebook_prepare/Phrases4.xlsx'
xlsx_file_path_b = '../Data/bluebook_prepare/Phrases3.xlsx'
delimiters_for_sentence = [",", ";", "but", "(", "while", ":", "whereas", "though"]
specific_entries = ['A', 'B', 'C', 'D', 'ABCD', 'ABC', 'ABD', 'ACD', 'BCD', 'AB', 'AC', 'BC', 'AD', 'BD', 'CD']
specific_phrases = ["four alternatives", "four policy alternatives", "four main policy alternatives"]

process_folder(folder_path, xlsx_file_path_a, xlsx_file_path_b, delimiters_for_sentence, specific_entries, specific_phrases)
