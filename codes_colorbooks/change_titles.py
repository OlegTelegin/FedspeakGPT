import os
import re

# Author: Oleg Telegin

# Find titles
def find_specific_pattern(chunks, delimiters, threshold):
    # List to store indices of delimiters that match the pattern
    matching_indices = []

    # Convert threshold to float for comparison
    threshold_value = float(threshold)

    for i in range(len(delimiters) - 1):
        # Extract font size from the current and next delimiter
        current_font_size_match = re.search(r'Font Size: ([\d.]+|Default)', delimiters[i])
        next_font_size_match = re.search(r'Font Size: ([\d.]+|Default)', delimiters[i + 1])

        if current_font_size_match and next_font_size_match:
            current_font_size = current_font_size_match.group(1)
            next_font_size = next_font_size_match.group(1)

            # Convert font sizes to float, treat 'Default' as equal to threshold
            current_font_size = threshold_value if current_font_size == 'Default' else float(current_font_size)
            next_font_size = threshold_value if next_font_size == 'Default' else float(next_font_size)
            # print(current_font_size)

            # Check if current font size is bigger than threshold and next is equal to threshold
            if current_font_size > threshold_value and next_font_size == threshold_value:
                # Check if the chunk corresponding to the next delimiter does not end with a comma and is shorter than 50 characters
                if not chunks[i].endswith('.') and len(chunks[i]) < 60 and len(chunks[i]) > 3:
                    # This delimiter matches the pattern
                    matching_indices.append(i)

    return matching_indices

# Process 1 file
def process_file(input_file_path, output_file_path, threshold):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    delimiter_pattern = r'(\(Font Size: [^\)]+\)\s)'
    parts = re.split(delimiter_pattern, text)
    delimiters = parts[1::2]
    chunks = parts[::2]
    chunks = chunks[1:]

    matching_indices = find_specific_pattern(chunks, delimiters, threshold)

    for index in matching_indices:
        if chunks[index].endswith('\n'):
            chunks[index] = chunks[index].rstrip('\n') + ':\n'
        else:
            chunks[index] += ':'
        # print(chunks[index])

    combined_text = ''.join([delimiters[i] + chunks[i] for i in range(len(chunks))])
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(combined_text)

# Process all files in a folder
def process_all_files(folder_path, output_folder, font_dict):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            print(f"Processing {filename}...")
            input_file_path = os.path.join(folder_path, filename)
            output_file_path = os.path.join(output_folder, filename)
            threshold = font_dict.get(filename)
            process_file(input_file_path, output_file_path, threshold)

# Paths, main font size, and function call
folder_path = '../Data/bluebook_prepare/move_inserted_pages'
output_folder = '../Data/bluebook_prepare/change_titles'
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
process_all_files(folder_path, output_folder, font_dict)
