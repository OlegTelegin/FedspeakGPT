import os
import re

# Author: Oleg Telegin

# Recognize if 'as in Alternative X' points out or compares in 1 file
def process_text_with_delimiters(txt_file_path, output_file_path, specific_entries_dict_3, specific_entries_dict_4, delete_entries_dict_3, delete_entries_dict_4):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into chunks and delimiters
    pattern = re.compile(r'(\{[^}]*first[^}]*\})')
    parts = pattern.split(text)
    chunks = parts[::2]
    chunks = chunks[1:]
    delimiters = parts[1::2]
    if delimiters and "{four" in delimiters[0]:
        entries_dict = specific_entries_dict_4
        delete_entries_dict = delete_entries_dict_4
        print('4 Alternatives')
    else:
        entries_dict = specific_entries_dict_3
        delete_entries_dict = delete_entries_dict_3
        print('3 Alternatives')

    updated_delimiters = []
    last_first_index = -1

    for index, delimiter in enumerate(delimiters):
        if re.search(r'(?<!not)first', delimiter):
            last_first_index = index

        key_found = next((key for key in entries_dict if key in delimiter), None)
        if key_found:
            value_found_in_range = False
            for i in range(last_first_index, index + 1):
                if any(value in delimiters[i] for value in entries_dict[key_found]):
                    value_found_in_range = True
                    break

            if not value_found_in_range:
                for delete_entry in delete_entries_dict:
                    delimiter = re.sub(r',\s*\b' + re.escape(delete_entry) + r'\b', '', delimiter)

        updated_delimiters.append(delimiter)

    combined_text = ''.join([updated_delimiters[i] + chunks[i] for i in range(len(chunks))])
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(combined_text)

# Process all files in a folder
def process_all_files_in_folder(input_folder, output_folder, specific_entries_dict_3, specific_entries_dict_4,
                                delete_entries_dict_3, delete_entries_dict_4):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is a .txt file
        if filename.endswith('.txt'):
            txt_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            # Process the text file
            process_text_with_delimiters(txt_file_path, output_file_path, specific_entries_dict_3, specific_entries_dict_4,
                                         delete_entries_dict_3, delete_entries_dict_4)

            print(f"Processed {filename}")

# Paths, dictionaries, and function call
input_folder = '../Data/bluebook_prepare/listing_phrases'
output_folder = '../Data/bluebook_prepare/work_with_as_in'

specific_entries_dict_3 = {
    '106': ['28', '29'],
    '107': ['27', '29'],
    '108': ['27', '28'],
    '249': ['28', '29'],
    '250': ['27', '29'],
    '251': ['27', '28'],
}
specific_entries_dict_4 = {
    '176': ['32', '33', '34'],
    '177': ['31', '33', '34'],
    '178': ['31', '32', '34'],
    '179': ['31', '32', '33'],
    '364': ['32', '33', '34'],
    '365': ['31', '33', '34'],
    '366': ['31', '32', '34'],
    '367': ['31', '32', '33'],
}
delete_entries_dict_3 = ['106', '107', '108', '115', '116', '117', '249', '250', '251']
delete_entries_dict_4 = ['176', '177', '178', '179', '188', '189', '190', '191', '364', '365', '366', '367']

process_all_files_in_folder(input_folder, output_folder, specific_entries_dict_3, specific_entries_dict_4, delete_entries_dict_3, delete_entries_dict_4)
