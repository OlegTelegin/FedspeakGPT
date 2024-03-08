import os
import re

# Author: Oleg Telegin

# Move the footnotes
def process_paragraphs(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into paragraphs based on the font size pattern
    delimiter_pattern = r'(\(Font Size: [^\)]+\)\s)'
    paragraphs = re.split(delimiter_pattern, text)
    processed_paragraphs = {}
    final_text = []
    delimiters = paragraphs[1::2]  # Extracting the delimiters
    content_chunks = paragraphs[::2]  # Extracting the content

    for index, paragraph in enumerate(reversed(content_chunks)):
        # Find Type 1 and Type 2 patterns (indication of the footnote and footnote)
        type_1_match = re.match(r'^\^\d{1,2}([ \t]+|[a-zA-Z]|\n)', paragraph)
        type_2_matches = re.findall(r'.(\^\d+)', paragraph)

        if type_1_match:
            number = type_1_match.group()
            processed_paragraphs[number] = paragraph
            final_text.append("\n")

        elif type_2_matches:
            for match in type_2_matches:
                number = match[0:]
                numeric_part = int(number[1:])  # Extract the numeric part and convert to integer
                insert_offset = 2 if numeric_part < 10 else 3  # Determine the offset based on the number size
                if number in processed_paragraphs:
                    type_1_text = processed_paragraphs.pop(number)
                    insert_position = paragraph.find(match[:])

                    paragraph = paragraph[:insert_position+insert_offset] + type_1_text + ' ' + paragraph[insert_position+insert_offset:]
                else:
                    # If there's no Type 1 for this Type 2, skip this paragraph
                    pass
            final_text.append(paragraph)
        else:
            final_text.append(paragraph)

    # Reverse the final_text list
    final_text_reversed = final_text[::-1]
    # Join and write the reversed text
    modified_text = ''.join([f"{delimiters[i]}{final_text_reversed[i+1]}" for i in range(len(final_text_reversed)-1)])
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(modified_text)

# Process all files in a folder
def process_all_files_in_folder(input_folder_path, output_folder_path):
    # Ensure the output folder exists
    os.makedirs(output_folder_path, exist_ok=True)

    for filename in os.listdir(input_folder_path):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, filename)
            process_paragraphs(input_file_path, output_file_path)
            print(f"Processed: {filename}")

# Paths and function call
input_folder_path = '../Data/bluebook_prepare/concatenate_pars_footnotes'
output_folder_path = '../Data/bluebook_prepare/move_footnotes/'
process_all_files_in_folder(input_folder_path, output_folder_path)
