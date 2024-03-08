import os
import re

# Author: Oleg Telegin

# Find small font text in consecutive paragraphs
def find_consecutive_small_font_delimiters(text, threshold):

    delimiter_pattern = r'(\(Font Size: [^\)]+\)\s)'
    parts = re.split(delimiter_pattern, text)
    delimiters = parts[1::2]
    chunks = parts[::2]
    chunks = chunks[1:]

    def font_size_or_default(delimiter):
        if 'Default' in delimiter:
            return 0  # Use Default as a font smaller than any threshold
        match = re.search(r'\d+(\.\d+)?', delimiter)
        return float(match.group()) if match else float('inf')

    consecutive_ranges = []
    start = None

    for i in range(1, len(delimiters) - 1):  # Skip the first and last delimiter
        current_font_size = font_size_or_default(delimiters[i])
        prev_font_size = font_size_or_default(delimiters[i-1])
        next_font_size = font_size_or_default(delimiters[i+1])
        chunk_length = len(chunks[i-1])
        chunk_ends_correctly = chunks[i-1].endswith('.\n')

        # Check if the current delimiter meets the criteria
        if current_font_size < threshold and prev_font_size >= threshold and next_font_size < threshold and not chunk_ends_correctly and chunk_length < 50 and not chunks[i-1].rstrip().endswith(":"):
            if start is None:  # Start of a new range
                start = i-1
        # Check if the range continues
        if i == len(delimiters) - 1 or font_size_or_default(delimiters[i+1]) >= threshold:
            consecutive_ranges.append((start, i))
            start = None  # Reset for the next range

    # List comprehension to filter and print
    filtered_ranges = [(start, end) for start, end in consecutive_ranges if start is not None]
    print(filtered_ranges)
    return filtered_ranges, chunks, delimiters

# Process the text and move the selected chunks to the end
def move_chunks_to_end(chunks, delimiters, filtered_ranges):
    # Initialize lists to hold chunks and delimiters to be moved
    chunks_to_move = []
    delimiters_to_move = []

    # Sort ranges by start index in reverse order to safely remove them without affecting indices
    filtered_ranges.sort(reverse=True)

    # Extract and remove the selected ranges
    for start, end in filtered_ranges:
        # if delimiters[end] == '(Font Size: Default) ':
        #     print(delimiters[end])
        #     print(chunks[end])
        #     print(chunks[end+1])
        # print(chunks[start])

        for i in range(end, start - 1, -1):  # Go backwards to avoid index shifting on removal
            chunks_to_move.insert(0, chunks.pop(i))
            delimiters_to_move.insert(0, delimiters.pop(i))

    # Append the extracted chunks and delimiters to the end
    chunks.extend(chunks_to_move)
    delimiters.extend(delimiters_to_move)

    # Combine back into text
    combined_text = ''.join([delimiters[i] + chunks[i] for i in range(len(chunks))])

    return combined_text

# Process 1 file
def process_file(input_file_path, output_folder, threshold):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    filtered_ranges, chunks, delimiters = find_consecutive_small_font_delimiters(text, threshold)
    combined_text = move_chunks_to_end(chunks, delimiters, filtered_ranges)

    output_file_name = os.path.basename(input_file_path)
    output_file_path = os.path.join(output_folder, output_file_name)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(combined_text)

# Process all files in a folder
def process_folder(input_folder, output_folder, font_dict):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            threshold = font_dict.get(filename)
            print(f"Processing {filename}...")
            process_file(input_file_path, output_folder, threshold)

# Paths, main font size, and function call
input_folder = '../Data/bluebook_prepare/empty_pars_and_footnotes'
output_folder = '../Data/bluebook_prepare/move_inserted_pages'
font_dict = {
    '2004-03-16_short.txt': 13,
    '2004-05-04_short.txt': 13,
    '2004-06-29_short.txt': 14,
    '2004-08-10_short.txt': 13,
    '2004-09-21_short.txt': 14,
    '2004-11-10_short.txt': 14,
    '2004-12-14_short.txt': 14,
    '2005-02-01_short.txt': 14,
    '2005-03-22_short.txt': 14,
    '2005-05-03_short.txt': 14,
    '2005-06-29_short.txt': 14,
    '2005-08-09_short.txt': 14,
    '2005-09-20_short.txt': 14,
    '2005-11-01_short.txt': 14,
    '2005-12-13_short.txt': 14,
    '2006-01-31_short.txt': 14,
    '2006-03-27_short.txt': 14,
    '2006-05-10_short.txt': 14,
    '2006-06-28_short.txt': 14,
    '2006-08-08_short.txt': 14,
    '2006-09-20_short.txt': 14,
    '2006-10-24_short.txt': 14,
    '2006-12-12_short.txt': 14,
    '2007-01-30_short.txt': 14,
    '2007-03-20_short.txt': 14,
    '2007-05-09_short.txt': 14,
    '2007-06-27_short.txt': 14,
    '2007-08-07_short.txt': 14,
    '2007-09-18_short.txt': 14,
    '2007-10-30_short.txt': 14,
    '2007-12-11_short.txt': 14,
    '2008-01-29_short.txt': 14,
    '2008-03-18_short.txt': 14,
    '2008-04-29_short.txt': 14,
    '2008-06-24_short.txt': 14,
    '2008-08-05_short.txt': 14,
    '2008-09-16_short.txt': 14,
    '2008-10-28_short.txt': 14,
    '2008-12-15_short.txt': 14,
    '2009-01-27_short.txt': 14,
    '2009-03-17_short.txt': 14,
    '2009-04-28_short.txt': 14,
    '2009-06-23_short.txt': 14,
    '2009-08-11_short.txt': 14,
    '2009-09-22_short.txt': 14,
    '2009-11-03_short.txt': 14,
    '2009-12-15_short.txt': 14,
    '2010-01-26_short.txt': 14,
    '2010-03-16_short.txt': 14,
    '2010-04-27_short.txt': 14,
    '2010-06-22_short.txt': 12,
    '2010-08-10_short.txt': 12,
    '2010-09-21_short.txt': 12,
    '2010-11-02_short.txt': 12,
    '2010-12-14_short.txt': 12,
    '2011-01-25_short.txt': 12,
    '2011-03-15_short.txt': 12,
    '2011-04-26_short.txt': 12,
    '2011-06-21_short.txt': 12,
    '2011-08-09_short.txt': 12,
    '2011-09-20_short.txt': 12,
    '2011-11-01_short.txt': 12,
    '2011-12-13_short.txt': 12,
    '2012-01-24_short.txt': 12,
    '2012-03-13_short.txt': 12,
    '2012-04-24_short.txt': 12,
    '2012-06-19_short.txt': 12,
    '2012-07-31_short.txt': 12,
    '2012-09-12_short.txt': 12,
    '2012-10-23_short.txt': 12,
    '2012-12-11_short.txt': 12,
    '2013-01-29_short.txt': 12,
    '2013-03-19_short.txt': 12,
    '2013-04-30_short.txt': 12,
    '2013-06-18_short.txt': 12,
    '2013-07-30_short.txt': 12,
    '2013-09-17_short.txt': 12,
    '2013-10-29_short.txt': 12,
    '2013-12-17_short.txt': 12,
    '2014-01-28_short.txt': 12,
    '2014-03-18_short.txt': 12,
    '2014-04-29_short.txt': 12,
    '2014-06-17_short.txt': 12,
    '2014-07-29_short.txt': 12,
    '2014-09-16_short.txt': 12,
    '2014-10-28_short.txt': 12,
    '2014-12-16_short.txt': 12,
    '2015-01-27_short.txt': 12,
    '2015-03-17_short.txt': 12,
    '2015-04-28_short.txt': 12,
    '2015-06-16_short.txt': 12,
    '2015-07-28_short.txt': 12,
    '2015-09-16_short.txt': 12,
    '2015-10-27_short.txt': 12,
    '2015-12-15_short.txt': 12,
    '2016-01-26_short.txt': 12,
    '2016-03-15_short.txt': 12,
    '2016-04-26_short.txt': 12,
    '2016-06-14_short.txt': 12,
    '2016-07-26_short.txt': 12,
    '2016-09-20_short.txt': 12,
    '2016-11-01_short.txt': 12,
    '2016-12-13_short.txt': 12,
    '2017-01-31_short.txt': 12,
    '2017-03-14_short.txt': 12,
    '2017-05-02_short.txt': 12,
    '2017-06-13_short.txt': 12,
    '2017-07-25_short.txt': 12,
    '2017-09-19_short.txt': 12,
    '2017-10-31_short.txt': 12,
    '2017-12-12_short.txt': 12,
    '2018-01-30_short.txt': 12,
    '2018-03-20_short.txt': 12,
    '2018-05-01_short.txt': 12,
    '2018-06-12_short.txt': 12,
    '2018-07-31_short.txt': 12,
    '2018-09-25_short.txt': 12,
    '2018-11-07_short.txt': 12,
    '2018-12-18_short.txt': 12,
}

process_folder(input_folder, output_folder, font_dict)
